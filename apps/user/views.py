import json
from smtplib import SMTPServerDisconnected
from django.contrib.auth.views import PasswordResetView
from django.http import HttpResponse, JsonResponse
from .models import CustomUser, Address
from apps.order.models import Order
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.urls import reverse_lazy
from .validators import validate_password_strength
from .forms import UserProfileForm, CustomPasswordChangeForm
from .utils import generate_otp, send_otp_email, store_otp_in_redis
import redis
from django.contrib.auth.models import Group
from django.urls import reverse
from django.core.validators import validate_email


# Create your views here.


class RegisterUserView(View):
    template_name = 'Register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        email = email.lower()
        request.session['email'] = email
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not all([email, username, password]):
            messages.error(request, 'All fields are required.')
            return redirect('register')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        try:
            validate_password_strength(password)
        except ValidationError as e:
            messages.error(request, e.message)
            return redirect('register')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('register')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken')
            return redirect('register')

        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'User registered successfully.')
        email = request.session.get('email')
        otp_code = generate_otp(email)
        store_otp_in_redis(otp_code, email)
        send_otp_email(email, otp_code)
        return redirect('email_verification')


class Email_Verification(View):
    template_name = 'email_verification.html'

    def get(self, request):
        # email = request.session.get('email')
        # otp_code = generate_otp(email)
        # store_otp_in_redis(otp_code, email)
        # send_otp_email(email, otp_code)
        return render(request, self.template_name)

    def post(self, request):
        otp_code = request.POST.get('otp_code')
        email = request.session.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            print(otp_code, user.otp_code)

            if str(user.otp_code) == str(otp_code):
                user.is_active = True
                user.otp_code = None
                user.save()
                messages.success(request, 'Email verified successfully.')
                return redirect('login')
            else:
                messages.error(request, 'Invalid OTP code.')

        except ObjectDoesNotExist:
            messages.error(request, 'User does not exist.')
        return redirect('email_verification')


class SendOTPCodeView(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        email = email.lower()
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email format.')
            return JsonResponse({'error': 'Invalid email format'}, status=500)
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'Invalid email'}, status=400)
        otp_code = generate_otp(email)
        print(otp_code)
        if otp_code:
            send_otp_email(email, otp_code)
            store_otp_in_redis(email, otp_code)

            request.session['otp_code'] = otp_code
            request.session['otp_email'] = email

            return redirect('login')
        else:

            return JsonResponse({'error': 'Failed to generate OTP code'}, status=500)


class LoginUserView(View):
    template_name = 'Login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        login_option = request.POST.get('login_option')
        otp_code = request.POST.get('otp_code')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if login_option == 'otp':
            if not otp_code:
                messages.error(request, 'OTP code is required.')
                return redirect('login')

            email = request.session.get('otp_email')
            email = email.lower()
            redis_conn = redis.Redis()
            stored_otp = redis_conn.get(email)
            print(stored_otp)
            if stored_otp and stored_otp.decode('utf-8') == otp_code:
                redis_conn.delete(email)
                print(otp_code)

                user = authenticate(request, otp_code=otp_code, email=email)
                user.otp_code = None
                user.save()
                print('user: ', user)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'OTP-based login successful.')
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid OTP code.')
                    return redirect('login')
            else:
                messages.error(request, 'Invalid OTP codee.')
                return redirect('login')
        elif login_option == 'credentials':
            print(username, password)

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Credentials-based login successful.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
                return redirect('login')

        messages.error(request, 'Invalid login option.')
        return redirect('login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Logged out successfully.')
        return redirect('home')


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)


class AddressCreateView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'create_address.html')

    def post(self, request):
        name = request.POST.get('name')
        detail_address = request.POST.get('detail_address')
        postal_code = request.POST.get('postal_code')
        description = request.POST.get('description')
        city = request.POST.get('city')
        province = request.POST.get('province')

        address = Address(
            user=request.user,
            name=name,
            detail_address=detail_address,
            postal_code=postal_code,
            description=description,
            city=city,
            province=province
        )
        address.save()
        messages.success(request, 'Address created successfully.')
        return redirect('address-list')


class AddressListView(LoginRequiredMixin, View):
    def get(self, request):
        addresses = Address.objects.filter(user=request.user)
        return render(request, 'address_list.html', {'addresses': addresses})


class AddressSelectView(LoginRequiredMixin, View):
    def post(self, request):
        address_id = request.POST.get('address_id')
        try:
            address = Address.objects.get(id=address_id, user=request.user)
            request.session['selected_address_id'] = address.id
            messages.success(request, 'Address selected successfully.')
        except Address.DoesNotExist:
            messages.error(request, 'Address not found')
        return redirect('view-order')


class AddressEditView(LoginRequiredMixin, View):
    def get(self, request, address_id):
        address = get_object_or_404(Address, id=address_id, user=request.user)
        return render(request, 'address_edit.html', {'address': address})

    def post(self, request, address_id):
        address = get_object_or_404(Address, id=address_id, user=request.user)
        address.name = request.POST.get('name')
        address.detail_address = request.POST.get('detail_address')
        address.postal_code = request.POST.get('postal_code')
        address.description = request.POST.get('description')
        address.city = request.POST.get('city')
        address.province = request.POST.get('province')
        address.save()
        messages.success(request, 'Address updated successfully')
        return redirect('address-list')


class AddressDeleteView(LoginRequiredMixin, View):
    def post(self, request, address_id):
        address = get_object_or_404(Address, id=address_id, user=request.user)
        address.delete()
        messages.success(request, 'Address deleted successfully.')
        return redirect('address-list')


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        addresses = Address.objects.filter(user=user)
        orders = Order.objects.filter(customer=user)
        profile_form = UserProfileForm(instance=user)
        password_form = CustomPasswordChangeForm(user=user)

        is_seller = user.groups.filter(name='Sellers').exists()
        print(is_seller)

        return render(request, 'user_profile.html', {
            'profile_form': profile_form,
            'password_form': password_form,
            'addresses': addresses,
            'orders': orders,
            'is_seller': is_seller
        })

    def post(self, request):
        user = request.user
        profile_form = UserProfileForm(request.POST, instance=user)
        password_form = CustomPasswordChangeForm(user=user, data=request.POST)

        if 'update_profile' in request.POST and profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')

        if 'change_password' in request.POST and password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')

        return render(request, 'user_profile.html', {
            'profile_form': profile_form,
            'password_form': password_form,
            'addresses': user.CustomerAddress.all(),
            'orders': Order.objects.filter(customer=user)
        })


class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return response
        except SMTPServerDisconnected:
            messages.error(request, "There was a problem connecting to the email server. Please try again later.")
            return redirect('password_reset')


class CustomPasswordResetConfrimView(auth_views.PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')



