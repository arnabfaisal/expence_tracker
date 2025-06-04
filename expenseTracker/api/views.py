from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework import status 
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from .permissions import IsOwner

from drf_spectacular.utils import extend_schema



# Create your views here.
from users.models import CustomUser
from users.serializers import CustomUserSerializer,RegisterSerializer,LogoutSerializer

from category.models import PredefinedCategory, Category
from category  import  serializers

from core.models import UserBalance, Transaction, Goal, Report
from core.serializers import UserBalanceSerializer, TransactionSerializer, GoalSerializer, ReportSerializer



class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response("Successfully logged out",status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

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
    serializer_class = UserBalanceSerializer

    def get_queryset(self):
        return UserBalance.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@extend_schema(tags=["Transactions"])
class TransactionViewSets(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GoalViewSets(viewsets.ModelViewSet):
    serializer_class = GoalSerializer

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReportViewSets(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
