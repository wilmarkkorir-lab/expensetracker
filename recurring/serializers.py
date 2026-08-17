from rest_framework import serializers
from recurring.models import RecurringExpense


class RecurringExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringExpense
        fields = ["id", "category", "amount", "frequency", "next_due_date", "is_active"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
