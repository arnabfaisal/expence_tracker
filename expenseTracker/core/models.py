from django.db import models
from django.conf import settings
from category.models import Category
from django.utils import timezone

# Create your models here.
class expenseType(models.TextChoices):
    INCOME = ('income', 'Income')
    EXPENSE = ('expense', 'Expense')

class periodType(models.TextChoices):
    Daily = ('daily', 'Daily')
    Monthly = ('monthly', 'Monthly')
    WEEKLY = ('weekly', "Weekly")
    YEARLY = ("yearly", 'Yearly')

class UserBalance(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_expense = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}"


class Transaction(models.Model):
    user  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_transaction' )

    category  = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_transaction' )

    date = models.DateField(default=timezone.now)

    amount = models.DecimalField(max_digits=12, blank=False, null=False, decimal_places=2)
    description = models.CharField(max_length=150, blank=True, null=True)
    transaction_type = models.CharField(max_length=10, blank=False, null=False, choices= expenseType.choices)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} -> {self.amount} -> {self.transaction_type}"


class Goal(models.Model):
    user  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_goal' )
    
    # category  = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_goal' )

    target_amount = models.DecimalField(max_digits=12, blank=False, null=False, decimal_places=2)
    remaining_amount = models.DecimalField(max_digits=12, blank=False, null=False, decimal_places=2, default=0)
    period = models.CharField(blank=False, null=False, choices=periodType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    goal_type = models.CharField(max_length=10, blank=False,null=False ,choices=expenseType.choices)
    is_completed = models.BooleanField(default=False)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)


    def __str__(self):
        return f"{self.user} ->  -> {self.target_amount} -> {self.period}"
    

class Report(models.Model):
    user  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports' )
    report = models.CharField(max_length=200, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

