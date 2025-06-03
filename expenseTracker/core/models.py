from django.db import models, transaction
from django.conf import settings
from category.models import Category
from django.utils import timezone

from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver


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
    def balance(self):
        return self.total_income - self.total_expense
    
    def recalculate_totals(self):
        from django.db.models import Sum

        income_total = Transaction.objects.filter(user=self.user, transaction_type='income').aggregate(Sum('amount'))['amount_sum'] or 0

        expense_total = Transaction.objects.filter(user=self.user, transaction_type='expense').aggregate(Sum('amount'))['amount_sum'] or 0

        self.total_income = income_total
        self.total_expense = expense_total
        self.save()

    def __str__(self):
        return f"{self.user.email} -> {self.balance}"


class Transaction(models.Model):
    user  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_transaction' )

    category  = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_transaction' )

    date = models.DateField(default=timezone.now)


    amount = models.DecimalField(max_digits=12, blank=False, null=False, decimal_places=2)
    description = models.CharField(max_length=150, blank=True, null=True)
    transaction_type = models.CharField(max_length=10, blank=False, null=False, choices= expenseType.choices)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        user_balance, created = UserBalance.objects.get_or_create(user = self.user)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} -> {self.amount} -> {self.transaction_type}"


class Goal(models.Model):
    user  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_goal' )
    
    category  = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_goal' )

    target_amount = models.DecimalField(max_digits=12, blank=False, null=False, decimal_places=2)
    period = models.CharField(blank=False, null=False, choices=periodType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    goal_type = models.CharField(max_length=10, choices=expenseType.choices, default='income')
    is_achieved = models.BooleanField(default=False)
    achieved_at = models.DateTimeField(null=True, blank=True)

    def check_and_update_achievement(self):

        try:
            user_balance = UserBalance.objects.get(user=self.user)

            current_period_total = self.get_current_period_total()

            if current_period_total >= self.target_amount and not self.is_achieved:
                self.is_achieved = True 
                self.achieved_at = timezone.now()
                self.save()
                return True
            
            elif current_period_total < self.target_amount and self.is_achieved:
                self.achieved = False
                self.achieved_at = None 
                self.save()

            return self.is_achieved

        except UserBalance.DoesNotExist:
            return False
    


    def get_current_period_total(self):
        from django.db.models import Sum
        from datetime import date, timedelta

        today = date.today()

        if self.period == "daily":
            start_date = today
            end_date  = today
        elif self.period == 'weekly':
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)
        elif self.period == 'monthly':
            start_date = today.replace(day=1)
            if today.month == 12:
                end_date = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                end_date = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        elif self.period == 'yearly':
            start_date = today.replace(month=1, day=1)
            end_date = today.replace(month=12, day=31)


        total = Transaction.objects.filter(
            user = self.user,
            transaction_type = self.goal_type,
            date_range = [start_date, end_date]
        ).aggregate(Sum('amount'))['amount_sum'] or 0

        return 0
    @property
    def progress(self):

        try:
            current = self.get_current_period_total()
            return min(100, (current / self.target_amount) * 100)
        except ZeroDivisionError:
            return 0
    

    def __str__(self):
        return f"{self.user} set up a {self.target_amount} on a {self.period} basis"



class Report(models.Model):
    user  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports' )
    report = models.CharField(max_length=200, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)









