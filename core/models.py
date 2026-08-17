from datetime import date, timedelta
from decimal import Decimal
from django.db import models
from django.db.models import Sum


def get_period_start(period, reference_date=None):
    if reference_date is None:
        reference_date = date.today()
    if period == "daily":
        return reference_date
    elif period == "weekly":
        return reference_date - timedelta(days=reference_date.weekday())
    elif period == "monthly":
        return reference_date.replace(day=1)
    return reference_date


def get_period_end(period, reference_date=None):
    if reference_date is None:
        reference_date = date.today()
    if period == "daily":
        return reference_date
    elif period == "weekly":
        return reference_date + timedelta(days=6 - reference_date.weekday())
    elif period == "monthly":
        if reference_date.month == 12:
            return reference_date.replace(year=reference_date.year + 1, month=1, day=1) - timedelta(days=1)
        return reference_date.replace(month=reference_date.month + 1, day=1) - timedelta(days=1)
    return reference_date


def compute_budget_progress(budget):
    from transactions.models import Expense
    start = get_period_start(budget.period, budget.created_at.date())
    end = get_period_end(budget.period, budget.created_at.date())
    spent = Expense.objects.filter(
        user=budget.user,
        category=budget.category,
        date__range=[start, end],
    ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    return {
        "budget_id": budget.id,
        "category": budget.category.name,
        "period": budget.period,
        "limit": str(budget.limit_amount),
        "spent": str(spent),
        "remaining": str(budget.limit_amount - spent),
        "percentage": round(float(spent / budget.limit_amount * 100), 2) if budget.limit_amount > 0 else 0,
    }


def compute_goal_progress(goal):
    from transactions.models import Income, Expense
    start = goal.start_date
    end = goal.end_date
    total_income = Income.objects.filter(user=goal.user, date__range=[start, end]).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    total_expenses = Expense.objects.filter(user=goal.user, date__range=[start, end]).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    saved = total_income - total_expenses
    return {
        "goal_id": goal.id,
        "name": goal.name,
        "target": str(goal.target_amount),
        "saved": str(saved),
        "remaining": str(goal.target_amount - saved),
        "percentage": round(float(saved / goal.target_amount * 100), 2) if goal.target_amount > 0 else 0,
        "start_date": str(start),
        "end_date": str(end),
        "is_achieved": goal.is_achieved,
    }
