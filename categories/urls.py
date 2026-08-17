from django.urls import path
from rest_framework.generics import ListCreateAPIView
from categories.models import Category
from categories.serializers import CategorySerializer
from rest_framework.permissions import IsAuthenticated


class CategoryListCreateView(ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user__isnull=True) | Category.objects.filter(user=self.request.user)


urlpatterns = [
    path("categories/", CategoryListCreateView.as_view(), name="category-list"),
]
