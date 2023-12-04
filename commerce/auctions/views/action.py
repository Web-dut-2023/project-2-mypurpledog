from math import ceil

from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.urls import reverse

from .error import _400, _403
from .form import BidForm, CloseForm, CommentForm, NewForm, WatchForm
from ..models import Bid, Comment, Listing, Watch


@login_required
def new_listing(request: HttpRequest) -> HttpResponse:
    """
    Add a new listing
    """
    f = NewForm(request.POST)
    # Check form validity
    if not f.is_valid():
        return _400(request)
    user = request.user
    # Check user is logged in
    data = f.cleaned_data
    title: str = data["title"]
    description: str = data["description"]
    starting_bid = int(data["starting_bid"]*100)
    image_url: str = data["image_url"]
    lt = Listing(
        title=title, description=description, starting_bid=starting_bid,
        image_url=image_url, created_by=user)
    lt.save()
    categories: QuerySet = data["categories"]
    lt.categories.set(categories)
    return HttpResponseRedirect(reverse("listing", kwargs={"id_": lt.id}))


@login_required
def add_comment(request: HttpRequest) -> HttpResponse:
    """
    Comment on a listing
    """
    # Enforce "POST"
    if request.method != "POST":
        return _400(request)
    f = CommentForm(request.POST)
    # Check form validity
    if not f.is_valid():
        return _400(request)
    user = request.user
    data = f.cleaned_data
    id_: int = data["_id"]
    title: str = data["title"]
    content: str = data["content"]
    # Check corresponding listing existence
    try:
        lt = Listing.objects.get(id=id_)
    except Listing.DoesNotExist as err:
        return _400(request, err)
    # Add new comment
    comment = Comment(user=user, listing=lt, title=title, content=content)
    comment.save()
    return HttpResponseRedirect(reverse("listing", kwargs={"id_": id_}))


def edit_comment(request: HttpRequest) -> HttpResponse:
    """
    Edit a comment
    """
    # Enforce "POST"
    if request.method != "POST":
        return _400(request)
    f = CommentForm(request.POST)
    # Check form validity
    if not f.is_valid():
        return _400(request)
    data = f.cleaned_data
    id_: int = data["_id"]
    title: str = data["title"]
    content: str = data["content"]
    # Check corresponding listing existence
    try:
        com = Comment.objects.get(id=id_)
    except Comment.DoesNotExist as err:
        return _400(request, err)
    user = request.user
    # Check user is logged in
    if user != com.user:
        return _403(request)
    # Add new comment
    com.title = title
    com.content = content
    com.save()
    return HttpResponseRedirect(reverse("listing", kwargs={"id_": com.listing.id}))


@login_required
def watch(request: HttpRequest) -> HttpResponse:
    """
    Add to or remove from watchlist
    """
    # Enforce "POST"
    if request.method != "POST":
        return _400(request)
    f = WatchForm(request.POST)
    # Check form validity
    if not f.is_valid():
        return _400(request)
    user = request.user
    data = f.cleaned_data
    id_: int = data["_id"]
    action: str = data["_action"]
    # Check corresponding listing existence
    try:
        lt = Listing.objects.get(id=id_)
    except Listing.DoesNotExist as err:
        return _400(request, err)
    # Add to watchlist
    if action == WatchForm.ADD:
        # Do not duplicate
        if not Watch.objects.filter(user=user, listing=lt).exists():
            watch = Watch(user=request.user, listing=lt)
            watch.save()
        return HttpResponseRedirect(reverse("listing", kwargs={"id_": id_}))
    # Remove from watchlist
    elif action == WatchForm.REMOVE:
        Watch.objects.filter(user=user, listing=lt).delete()
        return HttpResponseRedirect(reverse("listing", kwargs={"id_": id_}))
    else:
        return _400(request)


def close(request: HttpRequest) -> HttpResponse:
    """
    Close a listing
    """
    # Enforce "POST"
    if request.method != "POST":
        return _400(request)
    f = CloseForm(request.POST)
    # Check form validity
    if not f.is_valid():
        return _400(request)
    data = f.cleaned_data
    id_: int = data["_id"]
    # Check corresponding listing existence
    try:
        lt = Listing.objects.get(id=id_)
    except Listing.DoesNotExist as err:
        return _400(request, err)
    # Check user is the creator
    if request.user != lt.created_by:
        return _403(request)
    # Mark nonactive
    lt.active = False
    lt.save()
    return HttpResponseRedirect(reverse("listing", kwargs={"id_": id_}))


@login_required
def bid(request: HttpRequest) -> HttpResponse:
    """
    Bid a listing
    """
    # Enforce "POST"
    if request.method != "POST":
        return _400(request)
    f = BidForm(request.POST)
    # Check form validity
    if not f.is_valid():
        return _400(request)
    user = request.user
    data = f.cleaned_data
    id_: int = data["_id"]
    bid = ceil(data["bid"] * 100)
    # Check corresponding listing existence
    try:
        lt = Listing.objects.get(id=id_)
    except Listing.DoesNotExist as err:
        return _400(request, err)
    # Check user is not the creator
    if user == lt.created_by:
        return _403(request)
    max_bid_amount = int(lt.get_max_bid()*100)
    # Check if the bid is larger than current
    if bid <= max_bid_amount:
        return HttpResponseRedirect(reverse("listing", kwargs={
            "id_": id_,
            "bid_err": "You've submitted an invalid bid!",
        }))
    # Add new bid
    new_bid = Bid(user=user, listing=lt, amount=bid)
    new_bid.save()
    return HttpResponseRedirect(reverse("listing", kwargs={"id_": id_}))
