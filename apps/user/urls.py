from django.urls import path
from .views import RegisterUserView, LoginUserView, SendOTPCodeView, LogoutView, Email_Verification, AddressCreateView, AddressListView, AddressSelectView, UserProfileView, AddressEditView, AddressDeleteView
from django.conf.urls import handler404
from .views import custom_404_view


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register' ),
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

]
handler404 = custom_404_view