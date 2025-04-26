from django.http import HttpRequest
from datetime import datetime
import os

def get_client_ip(request: HttpRequest) -> str:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR', 'Неизвестен')

def get_unique_filename(filename):
    base, ext = os.path.splitext(filename)
    unique_suffix = datetime.now().strftime('%Y%m%d%H%M%S')
    return f"{base}_{unique_suffix}{ext}"
