from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_password_strength(value):
    """
    Validate that the password meets certain strength requirements.
    """
    # Minimum length of the password
    min_length = 8
    if len(value) < min_length:
        raise ValidationError(
            _("Password must be at least {0} characters long.").format(min_length)
        )

    # Additional password strength requirements (e.g., must contain uppercase, lowercase, digits, etc.)
    # You can customize these requirements based on your application's needs

    # Check for uppercase letters
    if not any(char.isupper() for char in value):
        raise ValidationError(_("Password must contain at least one uppercase letter."))

    # Check for lowercase letters
    if not any(char.islower() for char in value):
        raise ValidationError(_("Password must contain at least one lowercase letter."))

    # Check for digits
    if not any(char.isdigit() for char in value):
        raise ValidationError(_("Password must contain at least one digit."))


    # if not any(char in "!@#$%^&*()-_+=<>,.?/:;{}[]" for char in value):
    #     raise ValidationError(_("Password must contain at least one special character."))

    # If the password passes all requirements, return
    return value
