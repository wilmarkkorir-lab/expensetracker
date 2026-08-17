from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from accounts.serializers import CustomTokenObtainPairSerializer, RegisterSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from accounts.models import User
from accounts.serializers import UserSerializer
from rest_framework.generics import RetrieveUpdateAPIView


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class MeView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("me/", MeView.as_view(), name="me"),
]
