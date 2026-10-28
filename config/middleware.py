"""Project middleware for locale-aware HTML responses."""


class LanguageAwareCacheMiddleware:
    """Prevent stale HTML after switching django_language cookie."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        content_type = response.get("Content-Type", "")
        if content_type.startswith("text/html"):
            response["Cache-Control"] = "private, no-cache"
            vary = response.get("Vary")
            if vary:
                parts = [part.strip() for part in vary.split(",") if part.strip()]
                if "Cookie" not in parts:
                    parts.append("Cookie")
                response["Vary"] = ", ".join(parts)
            else:
                response["Vary"] = "Cookie"
        return response
