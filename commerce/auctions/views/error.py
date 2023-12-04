from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.defaults import bad_request, page_not_found, permission_denied


def _400(request: HttpRequest, exception=None) -> HttpResponse:
    return bad_request(request, exception)
    # return HttpResponseRedirect(reverse("index"))


def _403(request: HttpRequest, exception=None) -> HttpResponse:
    return permission_denied(request, exception)
    # return HttpResponseRedirect(reverse("index"))


def _404(request: HttpRequest, exception=None) -> HttpResponse:
    # return page_not_found(request, exception)
    return HttpResponseRedirect(reverse("index"))
