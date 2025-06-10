from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register('users', views.CustomUserViewSets, basename='users')
router.register('predefined', views.PredefinedCategoryViewSets, basename='predefined')
router.register('category', views.CategoryViewSets, basename='category')

router.register('user-balance', views.UserBalanceViewSet, basename='balance')
router.register('transaction', views.TransactionViewSet, basename='transaction')
router.register('goal', views.GoalViewSet, basename='goal')
router.register('goal-history', views.GoalHistoryViewSet, basename='goal-history')
router.register('report', views.ReportViewSet, basename='report')

urlpatterns = [
    path("", include(router.urls)),
    path("register/", views.RegisterView.as_view(), name='register'),
    path("logout/", views.LogoutView.as_view(), name='logout'),
    path("me/", views.MeviewSet.as_view(), name='me'),
]

