from typing import Optional
from django.http import HttpRequest, HttpResponse
from django.http import request
from django.shortcuts import render

from .error import _403, _404
from .form import CommentForm, NewForm
from .util import gen_listing_bid, gen_listing_comments, gen_listing_forms
from .var import CURRENCY_SYMBOL
from ..models import Category, Comment, Listing, User


def index(request: HttpRequest) -> HttpResponse:
    listings = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "currency": CURRENCY_SYMBOL,
    })


def listing(request: HttpRequest, id_: int, bid_err: Optional[str] = None) -> HttpResponse:
    """
    Listing details page
    """
    try:
        lt = Listing.objects.get(id=id_)
    except Listing.DoesNotExist as err:
        return _404(request, err)
    # Bidding info
    is_owner = lt.created_by == request.user
    lb = gen_listing_bid(request, lt)
    # Watchlist
    watches: User.objects = lt.watched_by
    watching = watches.filter(id=request.user.id).exists()
    # Forms
    lf = gen_listing_forms(lt, lb, watching)
    # Comments
    lc = gen_listing_comments(request, lt)
    return render(request, "auctions/listing.html", {
        "lt": lt,
        "lb": lb,
        "lf": lf,
        "lc": lc,
        "bid_err": bid_err,
        "is_owner": is_owner,
        "watching": watching,
    })


def new_listing(request: HttpRequest) -> HttpResponse:
    """
    Add new listing
    """
    new_form = NewForm()
    return render(request, "auctions/new.html", {
        "form": new_form,
    })


def watchlist(request: HttpRequest) -> HttpResponse:
    """
    View watchlist
    """
    user = request.user
    if not user.is_authenticated:
        return _403(request)
    lt_manager: Listing.objects = user.watchlist
    lt = lt_manager.all()
    return render(request, "auctions/watchlist.html", {
        "listings": lt,
        "currency": CURRENCY_SYMBOL,
    })


def categories(request: HttpRequest) -> HttpResponse:
    """
    View all categories
    """
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories,
    })


def category(request: HttpRequest, category: str) -> HttpResponse:
    """
    View listings by category
    """
    category_obj = Category.objects.filter(
        name=category).first()
    if category_obj is None:
        return _404(request)
    listings: Listing.objects = category_obj.listings
    listing_elements = listings.filter(active=True)
    return render(request, "auctions/category.html", {
        "cat_name": category,
        "listings": listing_elements,
        "currency": CURRENCY_SYMBOL,
    })


def comment_new(request: HttpRequest, lt_id: int) -> HttpResponse:
    """
    Page for adding a new comment
    """
    try:
        lt = Listing.objects.get(id=lt_id)
    except Listing.DoesNotExist as err:
        return _404(request, err)
    comments_manager: Comment.objects = lt.comments
    # Check if user has already made a comment
    try:
        user_comment = comments_manager.get(user=request.user)
    except Comment.DoesNotExist:
        user_comment = None
    if user_comment is not None:
        return _403(request)
    comment_form = CommentForm(initial={"_id": lt.id})
    return render(request, "auctions/comment.html", {
        "lt": lt,
        "comment_form": comment_form,
        "post_url": "new-comment",
    })


def comment_edit(request: HttpRequest, com_id: int) -> HttpResponse:
    """
    Page for editing a comment
    """
    try:
        com = Comment.objects.get(id=com_id)
    except Comment.DoesNotExist as err:
        return _404(request, err)
    # Check if comment is made by the user
    if com.user != request.user:
        return _403(request)
    comment_form = CommentForm(initial={
        "_id": com.id,
        "title": com.title,
        "content": com.content,
    })
    lt: Listing.objects = com.listing
    return render(request, "auctions/comment.html", {
        "lt": lt,
        "comment_form": comment_form,
        "post_url": "edit-comment",
    })
