from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register('users', views.CustomUserViewSets, basename='users')
router.register('predefined', views.PredefinedCategoryViewSets, basename='predefined')
router.register('category', views.CategoryViewSets, basename='category')

router.register('user-balance', views.UserBalanceViewSets, basename='balance')
router.register('Transaction', views.TransactionViewSets, basename='transaction')
router.register('goal', views.GoalViewSets, basename='goal')
router.register('report', views.ReportViewSets, basename='report')

urlpatterns = [
    path("", include(router.urls))
]

