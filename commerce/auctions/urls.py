from django.urls import path
from django.views import i18n

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:id_>", views.listing, name="listing"),
    path("category", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("new", views.new_listing, name="new"),
    path("comment/new", views.add_comment, name="new-comment"),
    path("comment/new/<int:lt_id>", views.comment_new, name="comment-new"),
    path("comment/edit", views.edit_comment, name="edit-comment"),
    path("comment/edit/<int:com_id>", views.comment_edit, name="comment-edit"),
    path("watch", views.watch, name="watch"),
    path("bid", views.bid, name="bid"),
    path("close", views.close, name="close"),
    path("jsi18n", i18n.JavaScriptCatalog.as_view(), name="jsi18n"),
]
