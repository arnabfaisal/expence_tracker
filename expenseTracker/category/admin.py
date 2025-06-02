from django.contrib import admin

from .models import PredefinedCategory, Category, CategoryKeyword, PredefinedCategoryKeyword

# Register your models here.

admin.site.register(PredefinedCategory)
admin.site.register(Category)
admin.site.register(CategoryKeyword)
admin.site.register(PredefinedCategoryKeyword)
