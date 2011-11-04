from django.contrib import admin
from django.db import models
from models import *

class AuthorAdmin(admin.ModelAdmin):
    pass

class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'user', 'score')
    prepopulated_fields = {'slug': ('title',)}
    save_as = True # for testing

    
class LicenseAdmin(admin.ModelAdmin):
    pass

class PlaylistBookmarksInline(admin.TabularInline):
    model = PlaylistBookmarks
    extra = 1

class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('title', 'number_of_bookmarks', 'number_of_followers', 'forked_from')
    prepopulated_fields = {'slug': ('title',)}
    inlines = (PlaylistBookmarksInline,)

class PublisherAdmin(admin.ModelAdmin):
    pass

class VoteAdmin(admin.ModelAdmin):
    pass

admin.site.register(Author, AuthorAdmin)
admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(License, LicenseAdmin)
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Vote, VoteAdmin)


