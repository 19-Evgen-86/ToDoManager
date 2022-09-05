from django.core.exceptions import ValidationError


def email_validator(value: str):
    domain = value.split('@')[1]
    if domain == 'rambler.ru':
        raise ValidationError(f"email domain it shouldn't be {domain}")