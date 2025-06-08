from rest_framework import serializers
from category.serializers import CategorySerializer
from category.models import Category
from .models import UserBalance, Transaction, Goal, Report, GoalHistory

class UserBalanceSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)
    get_total_balance = serializers.SerializerMethodField()

    class Meta:
        model = UserBalance
        fields = ['id','user', 'get_total_balance', 'total_income', 'total_expense']


    def get_total_balance(self, obj):
        return round(obj.get_total_balance, 2)


class TransactionSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all(),
        write_only = True,
        source = "category"
    )

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']


class GoalSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    is_goal_active = serializers.SerializerMethodField()
    get_goal_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Goal
        fields = ['id', 'user', 'target_amount', 'period', 'created_at', 'updated_at', 'goal_type', 'is_completed', 'start_date', 'end_date', 'is_goal_active', 'get_goal_percentage'] 


    def get_goal_percentage(self, obj):
        return round(obj.get_goal_percentage, 2)
    
    def is_goal_active(self, obj):
        return obj.is_goal_active

class GoalHistorySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = GoalHistory
        fields = ['id', 'user', 'target_amount', 'achieved_on', 'days_taken', 'goal_type', 'start_date', 'end_date', 'created_at']

class ReportSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Report
        fields = "__all__"



