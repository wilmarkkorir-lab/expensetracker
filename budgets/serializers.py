from rest_framework import serializers
from budgets.models import Budget
from core.models import compute_budget_progress


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ["id", "category", "period", "limit_amount", "created_at"]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class BudgetProgressSerializer(serializers.Serializer):
    budget_id = serializers.IntegerField()
    category = serializers.CharField()
    period = serializers.CharField()
    limit = serializers.CharField()
    spent = serializers.CharField()
    remaining = serializers.CharField()
    percentage = serializers.FloatField()
