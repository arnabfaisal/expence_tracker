from rest_framework import serializers
from category.serializers import CategorySerializer
from category.models import Category
from .models import UserBalance, Transaction, Goal, Report

class UserBalanceSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)

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

    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'description', 'transaction_type', 'category', 'category_id','date', 'created_at']


class GoalSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Goal
        fields = "__all__"


class ReportSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Report
        fields = "__all__"

