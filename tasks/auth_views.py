from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.core.cache import cache
from django.http import HttpResponse


class RateLimitedLoginView(LoginView):
    """Block repeated failed logins from the same IP."""

    max_attempts = 10
    window_seconds = 300

    def _cache_key(self) -> str:
        from tasks.permissions import client_ip

        return f"login-attempts:{client_ip(self.request)}"

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        attempts = cache.get(self._cache_key(), 0)
        if attempts >= self.max_attempts:
            messages.error(
                request,
                "Too many login attempts. Try again in a few minutes.",
            )
            return self.render_to_response(self.get_context_data())
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        key = self._cache_key()
        attempts = cache.get(key, 0) + 1
        cache.set(key, attempts, timeout=self.window_seconds)
        return super().form_invalid(form)

    def form_valid(self, form):
        cache.delete(self._cache_key())
        return super().form_valid(form)
