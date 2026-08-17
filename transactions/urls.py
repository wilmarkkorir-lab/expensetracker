from django.urls import path
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from transactions.models import Expense, Income
from transactions.serializers import ExpenseSerializer, IncomeSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class ExpenseListCreateView(ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["category", "date"]
    ordering_fields = ["date", "amount", "created_at"]
    ordering = ["-date", "-created_at"]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpenseDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)


class IncomeListCreateView(ListCreateAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["date"]
    ordering_fields = ["date", "amount"]
    ordering = ["-date"]

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


urlpatterns = [
    path("expenses/", ExpenseListCreateView.as_view(), name="expense-list"),
    path("expenses/<int:pk>/", ExpenseDetailView.as_view(), name="expense-detail"),
    path("income/", IncomeListCreateView.as_view(), name="income-list"),
]
