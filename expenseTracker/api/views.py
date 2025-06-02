from django.shortcuts import render
from rest_framework import generics, viewsets

# Create your views here.
from users.models import CustomUser, UserInfo
from users.serializers import CustomUserSerializer, UserInfoSerializer

class CustomUserViewSets(viewsets.ModelViewSet):
    queryset = CustomUser.objects.prefetch_related('user_info')
    serializer_class = CustomUserSerializer
