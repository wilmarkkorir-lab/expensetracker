from django.urls import path
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from alerts.models import Notification
from alerts.serializers import NotificationSerializer
from rest_framework.permissions import IsAuthenticated


class NotificationListView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class NotificationMarkReadView(RetrieveUpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


urlpatterns = [
    path("alerts/", NotificationListView.as_view(), name="notification-list"),
    path("alerts/<int:pk>/read/", NotificationMarkReadView.as_view(), name="notification-mark-read"),
]
