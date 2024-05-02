from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import CustomUser


class CustomUserAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, otp_code=None, email=None, **kwargs):
        # Check if username is provided (either username or email)
        print('email:', email)
        print('otp_code: ', otp_code)
        if username or email is not None:
            try:
                # Try to retrieve the user based on the provided username (either username or email)
                user = CustomUser.objects.get(Q(username=username) | Q(email=email))

                # If password is provided, check password
                if password is not None and user.check_password(password):
                    return user
                # If password is not provided and OTP code is provided, check OTP code
                elif password is None and otp_code is not None:
                    print(f"Provided OTP code: {otp_code}")
                    print(f"Stored OTP code for user {user.username}: {user.otp_code}")

                    # Here, you would validate the OTP code against the user's stored OTP code
                    # For simplicity, let's assume the OTP code is stored in a field named 'otp_code' in the user model
                    if str(user.otp_code) == str(otp_code):
                        print("OTP code matched. User authenticated successfully.")

                        return user
            except CustomUser.DoesNotExist:
                pass

        # If username is not provided or user does not exist, return None
        print('aaaa')
        return None
