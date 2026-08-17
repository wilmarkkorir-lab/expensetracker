from django.urls import path
from rest_framework.generics import ListCreateAPIView
from budgets.models import Budget
from budgets.serializers import BudgetSerializer, BudgetProgressSerializer
from core.models import compute_budget_progress
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class BudgetListCreateView(ListCreateAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BudgetProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        budgets = Budget.objects.filter(user=request.user)
        progress = [compute_budget_progress(b) for b in budgets]
        serializer = BudgetProgressSerializer(progress, many=True)
        return Response(serializer.data)


urlpatterns = [
    path("budgets/", BudgetListCreateView.as_view(), name="budget-list"),
    path("budgets/progress/", BudgetProgressView.as_view(), name="budget-progress"),
]
