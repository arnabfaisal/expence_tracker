from rest_framework import serializers
from .models import PredefinedCategory, Category

class PredefinedCategorySerializer(serializers.ModelSerializer):

    class Meta: 
        model = PredefinedCategory
        fields = ['id', 'name', 'type']


from rest_framework import serializers
from category.models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'type', 'description']




