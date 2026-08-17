from django.urls import path
from rest_framework.generics import ListCreateAPIView
from recurring.models import RecurringExpense
from recurring.serializers import RecurringExpenseSerializer
from rest_framework.permissions import IsAuthenticated


class RecurringExpenseListCreateView(ListCreateAPIView):
    serializer_class = RecurringExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RecurringExpense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


urlpatterns = [
    path("recurring/", RecurringExpenseListCreateView.as_view(), name="recurring-list"),
]
