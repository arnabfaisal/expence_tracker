from django.shortcuts import render
from rest_framework import generics, viewsets

# Create your views here.
from users.models import CustomUser
from users.serializers import CustomUserSerializer 


from category.models import PredefinedCategory, PredefinedCategoryKeyword,Category, CategoryKeyword
from category  import  serializers



class CustomUserViewSets(viewsets.ModelViewSet):
    queryset = CustomUser.objects.prefetch_related('user_info')
    serializer_class = CustomUserSerializer



class PredefinedCategoryViewSets(viewsets.ModelViewSet):
    queryset = PredefinedCategory.objects.all()
    serializer_class = serializers.PredefinedCategorySerializer

class CategoryViewSets(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


