from django.http import HttpRequest, HttpResponse


def webhook_handler(request: HttpRequest) -> HttpResponse:
    print(request.body)
    return HttpResponse("OK")
