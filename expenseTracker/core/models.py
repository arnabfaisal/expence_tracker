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

    @property
    def balance(self):
        return self.total_income - self.total_expense
    

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

    def __str__(self):
        return f"{self.user} -> {self.amount} -> {self.transaction_type}"


class Goal(models.Model):
    user  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_goal' )
    
    category  = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_goal' )

    target_amount = models.DecimalField(max_digits=12, blank=False, null=False, decimal_places=2)
    period = models.CharField(blank=False, null=False, choices=periodType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_achieved = models.BooleanField(default=False)
    achieved_at = models.DateTimeField(null=True, blank=True)

    def check_and_update_achievement(self):

        try:
            user_balance = UserBalance.objects.get(user=self.user).balance
            if user_balance >= self.target_amount and not self.is_achieved:
                self.is_achieved = True
                self.achieved_at = timezone.now()
                self.save()
                return True
            return False
        except UserBalance.DoesNotExist:
            return False
    
    @property
    def progress(self):

        try:
            if self.transaction_type == 'income':
                current = UserBalance.objects.get(user=self.user).total_income
            else:
                current = UserBalance.objects.get(user=self.user).total_expense
            return min(100, (current / self.target_amount) * 100)
        except (UserBalance.DoesNotExist, ZeroDivisionError):
            return 0

    def __str__(self):
        return f"{self.user} set up a {self.target_amount} on a {self.period} basis"



class Report(models.Model):
    user  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports' )
    report = models.CharField(max_length=200, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

