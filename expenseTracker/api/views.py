# from django.shortcuts import render
# from rest_framework import generics, viewsets
# from rest_framework.response import Response
# from datetime import datetime
# from django.db.models import Sum
# from rest_framework.decorators import action
# from rest_framework import status 
# from rest_framework_simplejwt.tokens import RefreshToken

# from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
# from .permissions import IsOwner

# from drf_spectacular.utils import extend_schema



# # Create your views here.
# from users.models import CustomUser
# from users.serializers import CustomUserSerializer , RegisterSerializer, LogoutSerializer

# from category.models import PredefinedCategory, Category
# from category  import  serializers

# from core.models import UserBalance, Transaction, Goal, Report
# from core.serializers import UserBalanceSerializer, TransactionSerializer, GoalSerializer, ReportSerializer



# class RegisterView(generics.CreateAPIView):
#     queryset = CustomUser.objects.all()
#     permission_classes = [AllowAny]
#     serializer_class = RegisterSerializer


# class LogoutView(generics.GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = LogoutSerializer
#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh_token"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response(status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

# class CustomUserViewSets(viewsets.ModelViewSet):
#     queryset = CustomUser.objects.prefetch_related('user_info')
#     serializer_class = CustomUserSerializer
#     permission_classes = [IsAdminUser]

# class PredefinedCategoryViewSets(viewsets.ModelViewSet):
#     queryset = PredefinedCategory.objects.all()
#     serializer_class = serializers.PredefinedCategorySerializer
#     permission_classes = [IsAdminUser]

# class CategoryViewSets(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = serializers.CategorySerializer
#     permission_classes = [IsOwner]

# class UserBalanceViewSets(viewsets.ModelViewSet):
#     serializer_class = UserBalanceSerializer
#     permission_classes = [IsOwner]

#     def get_queryset(self):
#         return UserBalance.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

# @extend_schema(tags=["Transactions"])
# class TransactionViewSets(viewsets.ModelViewSet):
#     serializer_class = TransactionSerializer
#     permission_classes = [IsOwner]

#     def get_queryset(self):
#         return Transaction.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

# class GoalViewSets(viewsets.ModelViewSet):
#     serializer_class = GoalSerializer
#     permission_classes = [IsOwner]

#     def get_queryset(self):
#         return Goal.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

# class ReportViewSets(viewsets.ModelViewSet):
#     serializer_class = ReportSerializer
#     permission_classes = [IsOwner]

#     def get_queryset(self):
#         return Goal.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


#     @action(detail=False, methods=['get'])
#     def monthly_summary(self, request):
#         user = request.user
#         month = request.query_params.get('month')  # Format: '2025-06'
#         if not month:
#             month = datetime.now().strftime('%Y-%m')

#         year, month = map(int, month.split('-'))
#         transactions = Transaction.objects.filter(user=user, date__year=year, date__month=month)

#         income = transactions.filter(transaction_type='income').aggregate(total=Sum('amount'))['total'] or 0
#         expense = transactions.filter(transaction_type='expense').aggregate(total=Sum('amount'))['total'] or 0

#         return Response({
#             "month": f"{year}-{month:02}",
#             "income": income,
#             "expense": expense,
#             "net_savings": income - expense
#         })






from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from datetime import datetime
from django.db.models import Sum, Q
from django.utils.dateparse import parse_date

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes
from drf_spectacular.openapi import AutoSchema

from .permissions import IsOwner

# Import models and serializers
from users.models import CustomUser
from users.serializers import CustomUserSerializer, RegisterSerializer, LogoutSerializer

from category.models import PredefinedCategory, Category
from category import serializers

from core.models import UserBalance, Transaction, Goal, Report
from core.serializers import (
    UserBalanceSerializer, TransactionSerializer, GoalSerializer, ReportSerializer,
    TransactionSummarySerializer, GoalProgressSerializer, BulkTransactionSerializer,
    DetailedUserBalanceSerializer
)


@extend_schema(tags=["Authentication"])
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


@extend_schema(tags=["Authentication"])
class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "Successfully logged out"}, 
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response(
                {"error": "Invalid token"}, 
                status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(tags=["Admin - Users"])
class CustomUserViewSets(viewsets.ModelViewSet):
    queryset = CustomUser.objects.prefetch_related('user_info')
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]


@extend_schema(tags=["Admin - Categories"])
class PredefinedCategoryViewSets(viewsets.ModelViewSet):
    queryset = PredefinedCategory.objects.all()
    serializer_class = serializers.PredefinedCategorySerializer
    permission_classes = [IsAdminUser]


@extend_schema(tags=["Categories"])
class CategoryViewSets(viewsets.ModelViewSet):
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsOwner]
    
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=["User Balance"])
class UserBalanceViewSets(viewsets.ModelViewSet):
    serializer_class = UserBalanceSerializer
    permission_classes = [IsOwner]
    http_method_names = ['get', 'head', 'options']  # Only allow read operations

    def get_queryset(self):
        return UserBalance.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailedUserBalanceSerializer
        return UserBalanceSerializer

    @extend_schema(
        summary="Get detailed balance information",
        description="Returns detailed balance with recent transactions and active goals"
    )
    @action(detail=True, methods=['get'])
    def detailed(self, request, pk=None):
        balance = self.get_object()
        serializer = DetailedUserBalanceSerializer(balance, context={'request': request})
        return Response(serializer.data)

    @extend_schema(
        summary="Recalculate user balance",
        description="Force recalculation of balance from transactions"
    )
    @action(detail=True, methods=['post'])
    def recalculate(self, request, pk=None):
        balance = self.get_object()
        balance.recalculate_totals()
        serializer = self.get_serializer(balance)
        return Response({
            "message": "Balance recalculated successfully",
            "balance": serializer.data
        })


@extend_schema_view(
    list=extend_schema(
        summary="List user transactions",
        parameters=[
            OpenApiParameter("transaction_type", OpenApiTypes.STR, description="Filter by income/expense"),
            OpenApiParameter("category", OpenApiTypes.INT, description="Filter by category ID"),
            OpenApiParameter("date_from", OpenApiTypes.DATE, description="Filter from date (YYYY-MM-DD)"),
            OpenApiParameter("date_to", OpenApiTypes.DATE, description="Filter to date (YYYY-MM-DD)"),
        ]
    ),
    create=extend_schema(summary="Create a new transaction"),
    retrieve=extend_schema(summary="Get transaction details"),
    update=extend_schema(summary="Update transaction"),
    partial_update=extend_schema(summary="Partially update transaction"),
    destroy=extend_schema(summary="Delete transaction"),
)
@extend_schema(tags=["Transactions"])
class TransactionViewSets(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user).select_related('category')
        
        # Apply filters
        transaction_type = self.request.query_params.get('transaction_type')
        category = self.request.query_params.get('category')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        if category:
            queryset = queryset.filter(category_id=category)
        if date_from:
            queryset = queryset.filter(date__gte=parse_date(date_from))
        if date_to:
            queryset = queryset.filter(date__lte=parse_date(date_to))
            
        return queryset.order_by('-date', '-created_at')

    # Remove perform_create as it's handled in the serializer now
    
    @extend_schema(
        summary="Get monthly transaction summary",
        parameters=[
            OpenApiParameter(
                "month", 
                OpenApiTypes.STR, 
                description="Month in YYYY-MM format (default: current month)"
            )
        ],
        responses={200: TransactionSummarySerializer}
    )
    @action(detail=False, methods=['get'])
    def monthly_summary(self, request):
        user = request.user
        month = request.query_params.get('month')
        if not month:
            month = datetime.now().strftime('%Y-%m')

        try:
            year, month_num = map(int, month.split('-'))
        except ValueError:
            return Response(
                {"error": "Invalid month format. Use YYYY-MM"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        transactions = Transaction.objects.filter(
            user=user, 
            date__year=year, 
            date__month=month_num
        )

        income = transactions.filter(transaction_type='income').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        expense = transactions.filter(transaction_type='expense').aggregate(
            total=Sum('amount')
        )['total'] or 0

        data = {
            "period": f"{year}-{month_num:02}",
            "total_income": income,
            "total_expense": expense,
            "net_balance": income - expense,
            "transaction_count": transactions.count()
        }
        
        serializer = TransactionSummarySerializer(data)
        return Response(serializer.data)

    @extend_schema(
        summary="Get yearly transaction summary",
        parameters=[
            OpenApiParameter(
                "year", 
                OpenApiTypes.INT, 
                description="Year (default: current year)"
            )
        ],
        responses={200: TransactionSummarySerializer}
    )
    @action(detail=False, methods=['get'])
    def yearly_summary(self, request):
        user = request.user
        year = request.query_params.get('year')
        if not year:
            year = datetime.now().year
        else:
            year = int(year)

        transactions = Transaction.objects.filter(user=user, date__year=year)
        
        income = transactions.filter(transaction_type='income').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        expense = transactions.filter(transaction_type='expense').aggregate(
            total=Sum('amount')
        )['total'] or 0

        data = {
            "period": str(year),
            "total_income": income,
            "total_expense": expense,
            "net_balance": income - expense,
            "transaction_count": transactions.count()
        }
        
        serializer = TransactionSummarySerializer(data)
        return Response(serializer.data)

    @extend_schema(
        summary="Create multiple transactions",
        request=BulkTransactionSerializer,
        responses={201: BulkTransactionSerializer}
    )
    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        serializer = BulkTransactionSerializer(
            data=request.data, 
            context={'request': request}
        )
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Goals"])
class GoalViewSets(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user).select_related('category')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        summary="Check goal achievement",
        description="Manually check and update goal achievement status"
    )
    @action(detail=True, methods=['post'])
    def check_achievement(self, request, pk=None):
        goal = self.get_object()
        achieved = goal.check_and_update_achievement()
        return Response({
            'achieved': achieved,
            'progress': goal.progress,
            'current_period_total': goal.get_current_period_total(),
            'target_amount': goal.target_amount
        })

    @extend_schema(
        summary="Get goal progress",
        responses={200: GoalProgressSerializer}
    )
    @action(detail=False, methods=['get'])
    def progress_summary(self, request):
        goals = self.get_queryset()
        serializer = GoalProgressSerializer(goals, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Get achieved goals",
        responses={200: GoalProgressSerializer}
    )
    @action(detail=False, methods=['get'])
    def achieved(self, request):
        goals = self.get_queryset().filter(is_achieved=True)
        serializer = GoalProgressSerializer(goals, many=True)
        return Response(serializer.data)


@extend_schema(tags=["Reports"])
class ReportViewSets(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        # Fixed: was returning Goal objects instead of Report objects
        return Report.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        summary="Generate spending report by category",
        parameters=[
            OpenApiParameter("period", OpenApiTypes.STR, description="Period: daily, weekly, monthly, yearly"),
            OpenApiParameter("date", OpenApiTypes.DATE, description="Reference date (default: today)"),
        ]
    )
    @action(detail=False, methods=['get'])
    def spending_by_category(self, request):
        user = request.user
        period = request.query_params.get('period', 'monthly')
        reference_date = request.query_params.get('date')
        
        if reference_date:
            try:
                reference_date = parse_date(reference_date)
            except:
                return Response(
                    {"error": "Invalid date format. Use YYYY-MM-DD"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            reference_date = datetime.now().date()

        # Calculate date range based on period
        if period == 'daily':
            start_date = end_date = reference_date
        elif period == 'weekly':
            start_date = reference_date - timedelta(days=reference_date.weekday())
            end_date = start_date + timedelta(days=6)
        elif period == 'monthly':
            start_date = reference_date.replace(day=1)
            if reference_date.month == 12:
                end_date = reference_date.replace(year=reference_date.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                end_date = reference_date.replace(month=reference_date.month + 1, day=1) - timedelta(days=1)
        elif period == 'yearly':
            start_date = reference_date.replace(month=1, day=1)
            end_date = reference_date.replace(month=12, day=31)
        else:
            return Response(
                {"error": "Invalid period. Use: daily, weekly, monthly, yearly"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get spending by category
        from django.db.models import Sum
        from datetime import timedelta
        
        spending = Transaction.objects.filter(
            user=user,
            transaction_type='expense',
            date__range=[start_date, end_date]
        ).values(
            'category__name'
        ).annotate(
            total_amount=Sum('amount'),
            transaction_count=Transaction.models.Count('id')
        ).order_by('-total_amount')

        return Response({
            'period': period,
            'date_range': {
                'start': start_date,
                'end': end_date
            },
            'categories': list(spending)
        })

    @extend_schema(
        summary="Generate income vs expense report",
        parameters=[
            OpenApiParameter("months", OpenApiTypes.INT, description="Number of months to include (default: 12)"),
        ]
    )
    @action(detail=False, methods=['get'])
    def income_vs_expense(self, request):
        user = request.user
        months = int(request.query_params.get('months', 12))
        
        from django.db.models import Sum
        from datetime import date, timedelta
        from dateutil.relativedelta import relativedelta
        
        results = []
        current_date = date.today().replace(day=1)  # First day of current month
        
        for i in range(months):
            month_start = current_date - relativedelta(months=i)
            month_end = month_start + relativedelta(months=1) - timedelta(days=1)
            
            transactions = Transaction.objects.filter(
                user=user,
                date__range=[month_start, month_end]
            )
            
            income = transactions.filter(transaction_type='income').aggregate(
                total=Sum('amount')
            )['total'] or 0
            
            expense = transactions.filter(transaction_type='expense').aggregate(
                total=Sum('amount')
            )['total'] or 0
            
            results.append({
                'month': month_start.strftime('%Y-%m'),
                'income': income,
                'expense': expense,
                'net_savings': income - expense
            })
        
        return Response({
            'months_included': months,
            'data': list(reversed(results))  # Show oldest to newest
        })