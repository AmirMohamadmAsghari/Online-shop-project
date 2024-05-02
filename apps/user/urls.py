from django.urls import path
from .views import RegisterUserView, LoginUserView, SendOTPCodeView, LogoutView


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register' ),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('send-otp/', SendOTPCodeView.as_view(), name='send_otp'),
]