from django.db import models
from django.conf import settings
from category.models import Category
from django.utils import timezone
import calendar
from datetime import timedelta

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

    @property
    def get_total_balance(self):
        return self.total_income - self.total_expense

    def __str__(self):
        return f"{self.user.email}"


class Transaction(models.Model):
    user  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_transaction' )

    category  = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_transaction' )

    date = models.DateField(auto_now_add=True, blank=False, null=False)

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
    start_date = models.DateField(auto_now_add=True, blank=False, null=False)
    end_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Only set initial values on creation


        if not self.start_date:
            self.start_date = timezone.now().date()
        if not self.pk:
            # Set end_date based on period
            if self.period == 'monthly':
                month = self.start_date.month
                year = self.start_date.year
                _, last_day = calendar.monthrange(year, month)
                self.end_date = self.start_date.replace(day=last_day)
            elif self.period == 'weekly':
                self.end_date = self.start_date + timedelta(days=6)
            elif self.period == 'yearly':
                self.end_date = self.start_date.replace(year=self.start_date.year + 1)
            elif self.period == 'daily':
                self.end_date = self.start_date  # same day

            # Set remaining_amount initially same as target_amount
            self.remaining_amount = self.target_amount
            self.is_completed = False


        super().save(*args, **kwargs)
    
    @property
    def get_goal_percentage(self):
        if self.target_amount == 0:
            return 0
        
        return ((self.target_amount - self.remaining_amount) / self.target_amount) * 100
    
    @property
    def is_goal_active(self):
        if self.end_date is None:
            return False
        return not self.is_completed and timezone.now().date() <= self.end_date

    
    @property
    def get_remaining_days(self):
        today = timezone.now().date()
        if self.end_date and today <= self.end_date:
            return (self.end_date - today).days
        return 0  # or maybe return -1 to indicate it's past due


    def __str__(self):
        return f"{self.user} -> {self.target_amount} -> {self.period}"
    

class Report(models.Model):
    user  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports' )
    report = models.CharField(max_length=200, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class GoalHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    achieved_on = models.DateField()
    days_taken = models.PositiveIntegerField()
    goal_type = models.CharField(max_length=10, choices=expenseType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} | {self.goal_type} | {self.start_date} -> {self.end_date} | Achieved in {self.days_taken} days"
