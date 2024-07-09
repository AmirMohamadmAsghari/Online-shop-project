from django.urls import path
from .views import RegisterUserView, LoginUserView, SendOTPCodeView, LogoutView, Email_Verification, AddressCreateView, \
    AddressListView, AddressSelectView, UserProfileView, AddressEditView, AddressDeleteView

from .views import custom_404_view
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetView
urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('emailverification/', Email_Verification.as_view(), name='email_verification'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('send-otp/', SendOTPCodeView.as_view(), name='send_otp'),
    path('addresses', AddressListView.as_view(), name='address-list'),
    path('address/create', AddressCreateView.as_view(), name='address-create'),
    path('address/select', AddressSelectView.as_view(), name='address-select'),
    path('address/<int:address_id>/edit', AddressEditView.as_view(), name='address-edit'),
    path('address/<int:address_id>/delete', AddressDeleteView.as_view(), name='address-delete'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


]
handler404 = custom_404_view
