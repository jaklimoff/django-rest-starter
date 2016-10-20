from django.core.exceptions import ValidationError
import re


def validate_password(value):
    if len(value) < 8:
        raise ValidationError('Password is too short')

    patterns_count = 0

    first_pattern = r'[a-z]+'
    if re.search(first_pattern, value):
        patterns_count += 1

    second_pattern = r'[A-Z]+'
    if re.search(second_pattern, value):
        patterns_count += 1

    third_pattern = r'[\d]+'
    if re.search(third_pattern, value):
        patterns_count += 1

    fourth_pattern = r'[\?\[\!\@\#\$\%\^\&\*\(\)\_\-\+\=\[\{\]\}\;\:\<\>\|\.\/\?\.\]\"\'\\\/]+'
    if re.search(fourth_pattern, value):
        patterns_count += 1

    if patterns_count < 3:
        raise ValidationError('Password does not match the patterns')


def validate_username(value):
    username_pattern = r'[a-zA-Z\_]{4,}'
    if not re.search(username_pattern, value):
        raise ValidationError('Invalid username')
