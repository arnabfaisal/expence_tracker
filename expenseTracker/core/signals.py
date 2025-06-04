from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from .models import UserBalance, Transaction, Goal, GoalHistory 
from category.models import Category 
from django.utils import timezone
from datetime import timedelta




@receiver(post_save, sender=Transaction)
def update_user_balance(sender, instance, created, **kwargs):
    if created:
        user_balance, _ = UserBalance.objects.get_or_create(user=instance.user)
        if instance.transaction_type == 'income':
            user_balance.total_income += instance.amount
        elif instance.transaction_type == 'expense':
            user_balance.total_expense += instance.amount
        user_balance.save()

        active_goals = Goal.objects.filter(
            user = instance.user,
            goal_type = instance.transaction_type,
            is_completed = False,
            start_date__lte=instance.date,
            end_date__gte=instance.date
        )

        for goal in active_goals:
            goal.remaining_amount -= instance.amount
            if goal.remaining_amount <= 0:
                goal.is_completed = True
                goal.save() 


                GoalHistory.objects.create(
                    user = instance.user,
                    start_date = goal.start_date,
                    end_date = goal.end_date,
                    target_amount = goal.target_amount,
                    achieved_on = timezone.now().date(),
                    days_taken = (timezone.now().date() - goal.start_date).days,
                    goal_type = goal.goal_type,
                )
                goal.delete()
            else:
                goal.save()




@receiver(pre_delete, sender=Transaction)
def adjust_user_balance_on_delete(sender, instance, **kwargs):
    user_balance = UserBalance.objects.get(user=instance.user)
    if instance.transaction_type == 'income':
        user_balance.total_income -= instance.amount
    elif instance.transaction_type == 'expense':
        user_balance.total_expense -= instance.amount
    user_balance.save()



    related_goals = Goal.objects.filter(
        user=instance.user,
        goal_type=instance.transaction_type,
        start_date__lte=instance.date,
        end_date__gte=instance.date
    )

    for goal in related_goals:
        # Only adjust if goal was affected
        goal.remaining_amount += instance.amount
        if goal.remaining_amount > 0:
            goal.is_completed = False
        goal.save()