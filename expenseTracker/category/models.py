from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from decimal import Decimal
# Create your models here.

class CategoryType(models.TextChoices):
    INCOME = ('income', 'Income')
    EXPENSE = ('expense', 'Expense')


class PredefinedCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=10, choices=CategoryType.choices)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=150, blank=True, null=True)


    def __str__(self):
        return f"Predefined Category: {self.name}"

class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categories')
    type = models.CharField(max_length=10, choices=CategoryType.choices)
    name = models.CharField(max_length=100, blank=True, null=True)
    is_custom = models.BooleanField(default=False)

    predefined_category = models.ForeignKey(
        PredefinedCategory,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='predefined_category'
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Category: {self.name}"


class CategoryKeyword(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='keywords')
    

    keyword = models.CharField(max_length=100)
    priority = models.IntegerField(default=1)

    is_exact_match = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-priority', 'keyword']


    def __str__(self):
        return f"{self.category.name} - {self.keyword}"
    

class PredefinedCategoryKeyword(models.Model):

    predefined_category = models.ForeignKey(
        PredefinedCategory, 
        on_delete=models.CASCADE, 
        related_name='keywords'
    )
    keyword = models.CharField(max_length=100)
    priority = models.IntegerField(default=1)
    is_exact_match = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-priority', 'keyword']

    def __str__(self):
        return f"{self.predefined_category.name} - {self.keyword}"