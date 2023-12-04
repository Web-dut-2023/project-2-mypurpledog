from math import ceil
from dataclasses import dataclass
from typing import Optional
from django.db.models.query import QuerySet

from django.http import HttpRequest

from .form import BidForm, CloseForm, WatchForm
from .var import CURRENCY_SYMBOL
from ..models import Bid, Comment, Listing


@dataclass
class ListingBid():
    no_bids: bool
    num_bids: int
    is_max_bid: bool
    max_bid: float
    min_starting_bid: float
    currency: str


@dataclass
class ListingForms():
    close_form: CloseForm
    watch_form: WatchForm
    bid_form: BidForm


@dataclass
class ListingComments():
    user_comment: Optional[Comment]
    other_comments: QuerySet
    num_of_comments: int


def gen_listing_bid(request: HttpRequest, lt: Listing) -> ListingBid:
    """
    Generate listing bid information
    """
    bids_manager: Bid.objects = lt.bids
    bids = bids_manager.all()
    num_bids = bids.count()
    no_bids = num_bids == 0
    if no_bids:
        is_max_bid = False
        max_bid_amount_int = lt.starting_bid
    else:
        max_bid = bids.order_by("-amount").first()
        is_max_bid = max_bid.user == request.user
        max_bid_amount_int: int = max_bid.amount
    max_bid_amount = max_bid_amount_int/100
    min_starting_bid = (max_bid_amount_int+1)/100
    lb = ListingBid(no_bids, num_bids, is_max_bid,
                    max_bid_amount, min_starting_bid, CURRENCY_SYMBOL)
    return lb


def gen_listing_forms(lt: Listing, lb: ListingBid, watching: bool) -> ListingForms:
    close_form = CloseForm(initial={"_id": lt.id})
    watch_form = WatchForm(initial={
        "_id": lt.id,
        "_action": WatchForm.REMOVE if watching else WatchForm.ADD,
    })
    bid_form = BidForm(initial={
        "_id": lt.id,
        "bid": ceil(lb.min_starting_bid*1.1)
    }, bid_min_value=lb.min_starting_bid)
    lf = ListingForms(close_form, watch_form, bid_form)
    return lf


def gen_listing_comments(request: HttpRequest, lt: Listing) -> ListingComments:
    comments_manager: Comment.objects = lt.comments
    user = request.user
    if user.is_authenticated:
        try:
            user_comment = comments_manager.get(user=user)
        except Comment.DoesNotExist:
            user_comment = None
        other_comments = comments_manager.exclude(user=user)
    else:
        user_comment = None
        other_comments = comments_manager.all()
    num_of_comments = bool(user_comment) + len(other_comments)
    lc = ListingComments(user_comment, other_comments, num_of_comments)
    return lc
