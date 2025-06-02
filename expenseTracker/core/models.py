from django.db import models
from django.conf import settings
from category.models import Category

# Create your models here.
class expenseType(models.TextChoices):
    INCOME = ('income', 'Income')
    EXPENSE = ('expense', 'Expense')

class periodType(models.TextChoices):
    Daily = ('daily', 'Daily')
    Monthly = ('monthly', 'Monthly')
    WEEKLY = ('weekly', "Weekly")
    YEARLY = ("yearly", 'yearly')



class Transaction(models.Model):
    user  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_transaction' )

    category  = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_transaction' )

    amount = models.IntegerField(blank=False, null=False)
    description = models.CharField(max_length=150, blank=True, null=True)
    transaction_type = models.CharField(max_length=10, blank=False, null=False, choices= expenseType.choices)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} -> {self.amount} -> {self.type}"


class Goal(models.Model):
    user  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_goal' )
    
    category  = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_goal' )

    target_amount = models.IntegerField(blank=False, null=False)
    period = models.CharField(blank=False, null=False, choices=periodType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} set up a {self.target_amount} on a {self.period} basis"

