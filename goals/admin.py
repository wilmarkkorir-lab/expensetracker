from django.contrib import admin
from goals.models import Goal, GoalAllocation


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "period", "target_amount", "start_date", "end_date", "is_achieved")
    list_filter = ("period", "is_achieved")
    search_fields = ("name", "user__username")


@admin.register(GoalAllocation)
class GoalAllocationAdmin(admin.ModelAdmin):
    list_display = ("goal", "label", "percentage")
    list_filter = ("goal",)
    search_fields = ("goal__name", "label")
