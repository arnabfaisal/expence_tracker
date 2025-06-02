from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.response import Response
from datetime import datetime
from django.db.models import Sum
from rest_framework.decorators import action
from rest_framework import status 
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from .permissions import IsOwner

from drf_spectacular.utils import extend_schema



# Create your views here.
from users.models import CustomUser
from users.serializers import CustomUserSerializer , RegisterSerializer, LogoutSerializer

from category.models import PredefinedCategory, Category
from category  import  serializers

from core.models import UserBalance, Transaction, Goal, Report
from core.serializers import UserBalanceSerializer, TransactionSerializer, GoalSerializer, ReportSerializer



class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class CustomUserViewSets(viewsets.ModelViewSet):
    queryset = CustomUser.objects.prefetch_related('user_info')
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]

class PredefinedCategoryViewSets(viewsets.ModelViewSet):
    queryset = PredefinedCategory.objects.all()
    serializer_class = serializers.PredefinedCategorySerializer
    permission_classes = [IsAdminUser]

class CategoryViewSets(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsOwner]

class UserBalanceViewSets(viewsets.ModelViewSet):
    serializer_class = UserBalanceSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return UserBalance.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@extend_schema(tags=["Transactions"])
class TransactionViewSets(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GoalViewSets(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReportViewSets(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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






