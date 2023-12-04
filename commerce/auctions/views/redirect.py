from django.http import HttpRequest, HttpResponse

from .action import new_listing as post_new_listing
from .render import new_listing as get_new_listing
from .error import _400


def new_listing(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return get_new_listing(request)
    elif request.method == "POST":
        return post_new_listing(request)
    else:
        return _400(request)
