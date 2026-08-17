from rest_framework import serializers
from goals.models import Goal, GoalAllocation
from core.models import compute_goal_progress


class GoalAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalAllocation
        fields = ["id", "label", "percentage"]
        read_only_fields = ["id"]


class GoalSerializer(serializers.ModelSerializer):
    allocations = GoalAllocationSerializer(many=True, required=False)

    class Meta:
        model = Goal
        fields = ["id", "name", "period", "target_amount", "start_date", "end_date", "is_achieved", "allocations"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        allocations_data = validated_data.pop("allocations", [])
        validated_data["user"] = self.context["request"].user
        goal = Goal.objects.create(**validated_data)
        for alloc in allocations_data:
            GoalAllocation.objects.create(goal=goal, **alloc)
        return goal

    def update(self, instance, validated_data):
        allocations_data = validated_data.pop("allocations", [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.allocations.all().delete()
        for alloc in allocations_data:
            GoalAllocation.objects.create(goal=instance, **alloc)
        return instance


class GoalProgressSerializer(serializers.Serializer):
    goal_id = serializers.IntegerField()
    name = serializers.CharField()
    target = serializers.CharField()
    saved = serializers.CharField()
    remaining = serializers.CharField()
    percentage = serializers.FloatField()
    start_date = serializers.CharField()
    end_date = serializers.CharField()
    is_achieved = serializers.BooleanField()
