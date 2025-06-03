from django.db import models, transaction
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from .models import UserBalance, Transaction, Goal

from django.utils import timezone

@receiver(post_save, sender=Transaction)
def update_user_balance_on_transaction_save(sender, instance, created, **kwargs):
    """Update UserBalance when a Transaction is created or updated"""
    user_balance, created_balance = UserBalance.objects.get_or_create(user=instance.user)
    
    if created:
        # New transaction - add to appropriate total
        if instance.transaction_type == 'income':
            user_balance.total_income += instance.amount
        else:
            user_balance.total_expense += instance.amount
    else:
        # Updated transaction - recalculate from scratch to avoid issues
        user_balance.recalculate_totals()
        return  # recalculate_totals() already saves
    
    user_balance.save()
    
    # Check all user's goals after balance update
    check_user_goals(instance.user)

@receiver(post_delete, sender=Transaction)
def update_user_balance_on_transaction_delete(sender, instance, **kwargs):
    """Update UserBalance when a Transaction is deleted"""
    try:
        user_balance = UserBalance.objects.get(user=instance.user)
        if instance.transaction_type == 'income':
            user_balance.total_income -= instance.amount
        else:
            user_balance.total_expense -= instance.amount
        user_balance.save()
        
        # Check all user's goals after balance update
        check_user_goals(instance.user)
    except UserBalance.DoesNotExist:
        pass

@receiver(pre_save, sender=Transaction)
def store_old_transaction_values(sender, instance, **kwargs):
    """Store old values before update to handle changes properly"""
    if instance.pk:  # Only for updates, not new instances
        try:
            old_instance = Transaction.objects.get(pk=instance.pk)
            instance._old_amount = old_instance.amount
            instance._old_type = old_instance.transaction_type
        except Transaction.DoesNotExist:
            instance._old_amount = None
            instance._old_type = None

def check_user_goals(user):
    """Check and update all goals for a user"""
    goals = Goal.objects.filter(user=user)
    for goal in goals:
        goal.check_and_update_achievement()

# Additional utility functions
class TransactionManager:
    """Manager class for handling complex transaction operations"""
    
    @staticmethod
    @transaction.atomic
    def create_transaction(user, category, amount, transaction_type, description=None, date=None):
        """Create a transaction with automatic balance and goal updates"""
        if date is None:
            date = timezone.now().date()
            
        new_transaction = Transaction.objects.create(
            user=user,
            category=category,
            amount=amount,
            transaction_type=transaction_type,
            description=description,
            date=date
        )
        return new_transaction
    
    @staticmethod
    @transaction.atomic
    def update_transaction(transaction_id, **kwargs):
        """Update a transaction with automatic balance recalculation"""
        trans = Transaction.objects.get(id=transaction_id)
        
        for field, value in kwargs.items():
            setattr(trans, field, value)
        
        trans.save()
        return trans
    
    @staticmethod
    @transaction.atomic
    def delete_transaction(transaction_id):
        """Delete a transaction with automatic balance update"""
        trans = Transaction.objects.get(id=transaction_id)
        user = trans.user
        trans.delete()
        
        # Force recalculation to ensure accuracy
        try:
            user_balance = UserBalance.objects.get(user=user)
            user_balance.recalculate_totals()
        except UserBalance.DoesNotExist:
            pass