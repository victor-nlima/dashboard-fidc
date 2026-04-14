from django.utils import timezone
from django.http import JsonResponse
from django.conf import settings
from common.models import LoginAttempt
from datetime import timedelta

class CustomLoginRateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/api/token/' and request.method == 'POST':
            ip = self.get_client_ip(request)
            attempt, created = LoginAttempt.objects.get_or_create(ip_address=ip)

            if attempt.blocked_until and attempt.blocked_until > timezone.now():
                tempo_restante = (attempt.blocked_until - timezone.now()).seconds // 60
                return JsonResponse({
                    "detalhe": f"IP bloqueado por excesso de tentativas. Tente novamente em {tempo_restante} minutos.",
                    "status": 403
                }, status=403)

        return self.get_response(request)

    def get_client_ip(self, request):
        remote_addr = request.META.get('REMOTE_ADDR', '')
        trusted_proxies = getattr(settings, 'TRUSTED_PROXIES', [])
        if remote_addr in trusted_proxies:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
            if x_forwarded_for:
                return x_forwarded_for.split(',')[0].strip()
        return remote_addr