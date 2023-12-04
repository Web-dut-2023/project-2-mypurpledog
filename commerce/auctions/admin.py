from django.contrib import admin

from .models import Bid, Category, Comment, Listing, User, Watch

# Register your models here.


class BidAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Bid._meta.fields]
    list_editable = [field.name for field in Bid._meta.fields
                     if field.name not in ("id", "creation_time")]


class CategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Category._meta.fields]
    list_editable = [field.name for field in Category._meta.fields
                     if field.name not in ("id", "creation_time")]


class CommentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comment._meta.fields]
    list_editable = [field.name for field in Comment._meta.fields
                     if field.name not in ("id", "creation_time")]


class ListingAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Listing._meta.fields]
    list_editable = [field.name for field in Listing._meta.fields
                     if field.name not in ("id", "creation_time")]
    filter_horizontal = ("categories",)


class UserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in User._meta.fields
                    if field.name != "password"]
    list_editable = [field.name for field in User._meta.fields
                     if field.name not in ("id", "creation_time", "password")]


class WatchAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Watch._meta.fields]
    list_editable = [field.name for field in Watch._meta.fields
                     if field.name not in ("id", "creation_time")]


admin.site.register(Bid, BidAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Watch, WatchAdmin)
