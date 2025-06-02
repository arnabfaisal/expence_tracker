from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.response import Response
from datetime import datetime
from django.db.models import Sum
from rest_framework.decorators import action

# Create your views here.
from users.models import CustomUser
from users.serializers import CustomUserSerializer 

from category.models import PredefinedCategory, Category
from category  import  serializers

from core.models import UserBalance, Transaction, Goal, Report
from core.serializers import UserBalanceSerializer, TransactionSerializer, GoalSerializer, ReportSerializer



class CustomUserViewSets(viewsets.ModelViewSet):
    queryset = CustomUser.objects.prefetch_related('user_info')
    serializer_class = CustomUserSerializer

class PredefinedCategoryViewSets(viewsets.ModelViewSet):
    queryset = PredefinedCategory.objects.all()
    serializer_class = serializers.PredefinedCategorySerializer

class CategoryViewSets(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

class UserBalanceViewSets(viewsets.ModelViewSet):
    queryset = UserBalance.objects.all()
    serializer_class = UserBalanceSerializer

class TransactionViewSets(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class =  TransactionSerializer


class GoalViewSets(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer 

class ReportViewSets(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


    @action(detail=False, methods=['get'])
    def monthly_summary(self, request):
        user = request.user
        month = request.query_params.get('month')  # Format: '2025-06'
        if not month:
            month = datetime.now().strftime('%Y-%m')

        year, month = map(int, month.split('-'))
        transactions = Transaction.objects.filter(user=user, date__year=year, date__month=month)

        income = transactions.filter(transaction_type='income').aggregate(total=Sum('amount'))['total'] or 0
        expense = transactions.filter(transaction_type='expense').aggregate(total=Sum('amount'))['total'] or 0

        return Response({
            "month": f"{year}-{month:02}",
            "income": income,
            "expense": expense,
            "net_savings": income - expense
        })






