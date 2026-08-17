from decimal import Decimal
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from transactions.models import Expense, Income
from alerts.models import Notification
from datetime import date


class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = date.today()
        week_start = today - __import__("datetime").timedelta(days=today.weekday())
        month_start = today.replace(day=1)

        today_expenses = Expense.objects.filter(user=user, date=today).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
        today_income = Income.objects.filter(user=user, date=today).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
        week_expenses = Expense.objects.filter(user=user, date__range=[week_start, today]).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
        week_income = Income.objects.filter(user=user, date__range=[week_start, today]).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
        month_expenses = Expense.objects.filter(user=user, date__range=[month_start, today]).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
        month_income = Income.objects.filter(user=user, date__range=[month_start, today]).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

        unread_alerts = Notification.objects.filter(user=user, is_read=False).count()

        return Response({
            "today": {
                "expenses": str(today_expenses),
                "income": str(today_income),
                "net": str(today_income - today_expenses),
            },
            "week": {
                "expenses": str(week_expenses),
                "income": str(week_income),
                "net": str(week_income - week_expenses),
            },
            "month": {
                "expenses": str(month_expenses),
                "income": str(month_income),
                "net": str(month_income - month_expenses),
            },
            "unread_alerts": unread_alerts,
        })
