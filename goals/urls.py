from django.urls import path
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum
from goals.models import Goal
from goals.serializers import GoalSerializer, GoalProgressSerializer
from core.models import compute_goal_progress
from transactions.models import Income, Expense


class GoalListCreateView(ListCreateAPIView):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GoalDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)


class GoalProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            goal = Goal.objects.get(pk=pk, user=request.user)
        except Goal.DoesNotExist:
            return Response({"detail": "Not found"}, status=404)
        progress = compute_goal_progress(goal)
        serializer = GoalProgressSerializer(progress)
        return Response(serializer.data)


class AllocationPreviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            goal = Goal.objects.get(pk=pk, user=request.user)
        except Goal.DoesNotExist:
            return Response({"detail": "Not found"}, status=404)
        from decimal import Decimal
        start = goal.start_date
        end = goal.end_date
        total_income = Income.objects.filter(user=request.user, date__range=[start, end]).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
        total_expenses = Expense.objects.filter(user=request.user, date__range=[start, end]).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
        surplus = total_income - total_expenses
        allocations = goal.allocations.all()
        result = []
        for alloc in allocations:
            result.append({
                "label": alloc.label,
                "percentage": str(alloc.percentage),
                "amount": str(surplus * alloc.percentage / Decimal("100.00")),
            })
        return Response({
            "goal_id": goal.id,
            "surplus": str(surplus),
            "allocations": result,
        })


urlpatterns = [
    path("goals/", GoalListCreateView.as_view(), name="goal-list"),
    path("goals/<int:pk>/", GoalDetailView.as_view(), name="goal-detail"),
    path("goals/<int:pk>/progress/", GoalProgressView.as_view(), name="goal-progress"),
    path("goals/<int:pk>/allocation-preview/", AllocationPreviewView.as_view(), name="goal-allocation-preview"),
]
