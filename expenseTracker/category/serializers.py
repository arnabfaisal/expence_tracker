from rest_framework import serializers
from .models import PredefinedCategory, Category

class PredefinedCategorySerializer(serializers.ModelSerializer):

    class Meta: 
        model = PredefinedCategory
        fields = ['id', 'name', 'type']


class CategorySerializer(serializers.ModelSerializer):

    # predefined_category = PredefinedCategorySerializer(read_only=True)
    # predefined_category_id = serializers.PrimaryKeyRelatedField(
    #     queryset = PredefinedCategory.objects.all(), write_only=True,
    #     source = 'predefined_category',
    #     required = False
    # )
    user = serializers.StringRelatedField(read_only=True)

    class Meta: 
        model = Category
        fields = ['id', 'name', 'type', 'is_custom', 'user']



