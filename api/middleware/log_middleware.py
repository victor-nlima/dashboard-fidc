# log_middleware.py for api

import logging

class APILogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('api_logger')


    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # Pode haver múltiplos IPs, pega o primeiro
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '')
        return ip

    def __call__(self, request):
        if request.path.startswith('/api/'):
            ip = self._get_client_ip(request)
            method = request.method
            url = request.path
            self.logger.info(f"IP: {ip} | Método: {method} | URL: {url}")
        response = self.get_response(request)
        return response
