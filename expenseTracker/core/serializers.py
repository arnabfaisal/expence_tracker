from rest_framework import serializers
from category.serializers import CategorySerializer
from category.models import Category
from core.utils import suggest_category
from .models import UserBalance, Transaction, Goal, Report
from rest_framework.decorators import action


class UserBalanceSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)
    balance = serializers.SerializerMethodField()

    class Meta:
        model = UserBalance
        fields = ['id','balance', 'total_income', 'total_expense', 'user']


class TransactionSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all(),
        write_only = True,
        source = "Category"
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


class GoalSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    check_and_update_achievement = serializers.SerializerMethodField()

    class Meta:
        model = Goal
        fields = "__all__"


class ReportSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Report
        fields = "__all__"





    


