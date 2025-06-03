from rest_framework import serializers
from category.serializers import CategorySerializer
from category.models import Category
from core.utils import suggest_category
from .models import UserBalance, Transaction, Goal, Report
from rest_framework.decorators import action




from .signals import TransactionManager

class UserBalanceSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)
    balance = serializers.SerializerMethodField()

    class Meta:
        model = UserBalance
        fields = ['id','balance', 'total_income', 'total_expense', 'user']
        read_only_fields = ['total_income', 'total_expense', 'created_at', 'updated_at']


    def get_balance(self,obj):
        return obj.balance


class TransactionSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all(),
        write_only = True,
        source = "category"
    )

    def create(self, validated_data):
        user = self.context['request'].user
        if 'Category' not in validated_data:
            suggested = suggest_category(user, validated_data.get('description'))
            if suggested:
                validated_data['Category'] = suggested
        return super().create(validated_data)


    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'description', 'transaction_type', 'category', 'category_id','date', 'created_at']


    def validate_amount(self, value):
        """Ensure amount is positive"""
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value
    
    def validate_transaction_type(self, value):
        """Validate transaction type"""
        if value not in ['income', 'expense']:
            raise serializers.ValidationError("Transaction type must be 'income' or 'expense'")
        return value
    
    def create(self, validated_data):
        """Create transaction with automatic synchronization"""
        user = self.context['request'].user
        validated_data['user'] = user
        
        # Handle category suggestion if no category provided
        if 'category' not in validated_data:
            description = validated_data.get('description', '')
            suggested = suggest_category(user, description)
            if suggested:
                validated_data['category'] = suggested
            else:
                # You might want to create a default category or raise an error
                raise serializers.ValidationError("Category is required or no suitable category found")
        
        # Use TransactionManager for atomic operations
        return TransactionManager.create_transaction(
            user=user,
            category=validated_data['category'],
            amount=validated_data['amount'],
            transaction_type=validated_data['transaction_type'],
            description=validated_data.get('description'),
            date=validated_data.get('date')
        )
    
    def update(self, instance, validated_data):
        """Update transaction with automatic synchronization"""
        # Use TransactionManager for atomic updates
        return TransactionManager.update_transaction(
            transaction_id=instance.id,
            **validated_data
        )


class GoalSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    check_and_update_achievement = serializers.SerializerMethodField()

    class Meta:
        model = Goal
        fields = "__all__"

    def get_progress(self, obj):
        """Get progress percentage"""
        return round(obj.progress, 2)
    
    def get_current_period_total(self, obj):
        """Get current period total"""
        return float(obj.get_current_period_total())
    
    def get_achievement_status(self, obj):
        """Get detailed achievement status"""
        return {
            'is_achieved': obj.is_achieved,
            'achieved_at': obj.achieved_at,
            'progress_percentage': round(obj.progress, 2),
            'remaining_amount': max(0, float(obj.target_amount - obj.get_current_period_total()))
        }
    
    def validate_target_amount(self, value):
        """Ensure target amount is positive"""
        if value <= 0:
            raise serializers.ValidationError("Target amount must be greater than 0")
        return value
    
    def validate_period(self, value):
        """Validate period choice"""
        valid_periods = ['daily', 'weekly', 'monthly', 'yearly']
        if value not in valid_periods:
            raise serializers.ValidationError(f"Period must be one of: {', '.join(valid_periods)}")
        return value
    
    def validate_goal_type(self, value):
        """Validate goal type"""
        if value not in ['income', 'expense']:
            raise serializers.ValidationError("Goal type must be 'income' or 'expense'")
        return value
    
    def create(self, validated_data):
        """Create goal with user assignment"""
        user = self.context['request'].user
        validated_data['user'] = user
        goal = super().create(validated_data)
        
        # Check achievement immediately after creation
        goal.check_and_update_achievement()
        return goal
    
    def update(self, instance, validated_data):
        """Update goal and recheck achievement"""
        goal = super().update(instance, validated_data)
        goal.check_and_update_achievement()
        return goal
class ReportSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Report
        fields = "__all__"





class TransactionSummarySerializer(serializers.Serializer):
    """Serializer for transaction summaries"""
    total_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_expense = serializers.DecimalField(max_digits=12, decimal_places=2)
    net_balance = serializers.DecimalField(max_digits=12, decimal_places=2)
    transaction_count = serializers.IntegerField()
    period = serializers.CharField(max_length=50)

class GoalProgressSerializer(serializers.ModelSerializer):
    """Simplified serializer for goal progress tracking"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    progress = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = Goal
        fields = [
            'id', 'target_amount', 'period', 'goal_type', 
            'category_name', 'progress', 'status', 'is_achieved'
        ]
    
    def get_progress(self, obj):
        return round(obj.progress, 2)
    
    def get_status(self, obj):
        if obj.is_achieved:
            return "Achieved"
        elif obj.progress >= 80:
            return "Near Target"
        elif obj.progress >= 50:
            return "On Track"
        else:
            return "Needs Attention"

class BulkTransactionSerializer(serializers.Serializer):
    """Serializer for bulk transaction operations"""
    transactions = TransactionSerializer(many=True)
    
    def create(self, validated_data):
        """Create multiple transactions atomically"""
        from django.db import transaction
        
        transactions_data = validated_data['transactions']
        user = self.context['request'].user
        created_transactions = []
        
        with transaction.atomic():
            for transaction_data in transactions_data:
                transaction_data['user'] = user
                trans = TransactionManager.create_transaction(
                    user=user,
                    category=transaction_data['category'],
                    amount=transaction_data['amount'],
                    transaction_type=transaction_data['transaction_type'],
                    description=transaction_data.get('description'),
                    date=transaction_data.get('date')
                )
                created_transactions.append(trans)
        
        return {'transactions': created_transactions}

# Nested serializers for detailed views
class DetailedUserBalanceSerializer(UserBalanceSerializer):
    """Detailed user balance with recent transactions and goals"""
    recent_transactions = serializers.SerializerMethodField()
    active_goals = serializers.SerializerMethodField()
    
    class Meta(UserBalanceSerializer.Meta):
        fields = UserBalanceSerializer.Meta.fields + ['recent_transactions', 'active_goals']
    
    def get_recent_transactions(self, obj):
        recent = Transaction.objects.filter(user=obj.user).order_by('-created_at')[:5]
        return TransactionSerializer(recent, many=True, context=self.context).data
    
    def get_active_goals(self, obj):
        active = Goal.objects.filter(user=obj.user, is_achieved=False)
        return GoalProgressSerializer(active, many=True).data    


