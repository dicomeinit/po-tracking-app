from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def robots_txt(_: HttpRequest) -> HttpResponse:
    return HttpResponse("User-Agent: *\nDisallow: /", content_type="text/plain")
