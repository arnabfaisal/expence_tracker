from django.contrib import admin

from .models import Transaction, Goal, Report, UserBalance, GoalHistory
# Register your models here.
admin.site.register(Transaction)
admin.site.register(Goal)
admin.site.register(Report)
admin.site.register(UserBalance)
admin.site.register(GoalHistory)
