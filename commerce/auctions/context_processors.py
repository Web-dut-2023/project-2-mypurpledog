from typing import Dict
from django.http import HttpRequest

from .models import Listing


def wishlist_length(request: HttpRequest) -> Dict[str, str]:
    user = request.user
    if user.is_authenticated:
        lt_manager: Listing.objects = user.watchlist
        len_wishlist = lt_manager.all().count()
        len_wishlist_active = lt_manager.filter(active=True).count()
    else:
        len_wishlist = len_wishlist_active = 0
    return {
        "wishlist_len": f"{len_wishlist_active}/{len_wishlist}"
    }
