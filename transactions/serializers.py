from rest_framework import serializers
from transactions.models import Expense, Income


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ["id", "category", "amount", "note", "payment_method", "date", "created_at"]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ["id", "source", "amount", "date"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
