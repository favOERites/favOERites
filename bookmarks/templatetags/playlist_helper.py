import settings
from django import template
from django.template.defaultfilters import truncatewords, truncatewords_html, safe, linebreaks, striptags
from django.contrib.contenttypes.models import ContentType
from bookmarks.models import Vote, Playlist
import datetime
from itertools import chain



register = template.Library()

@register.filter
def is_following(user, object):
    followers = object.followers.values_list('id', flat=True)
    if user.id in followers:
        return True
    else:
        return False
    
@register.filter
def is_editor_or_owner(user, object):
    if object.user.id == user.id:
        return 'Owner'
    try:
        editors = object.editors.get(id=user.id)
        return 'Editor'
    except:
        return False
    

@register.filter
def is_forked(user, object):
    """ has playlist been forked by this user """ 
    try:
        fork = Playlist.objects.get(parent_fork__id=object.id, user__id=user.id)
        return fork
    except:
        return False

@register.inclusion_tag("fragments/add_to_playlist.html", takes_context=True)
def add_to_playlist(context):
    user = context['request'].user
    bookmark = context['bookmark'].pk
    bag = {}
    # playlists I own that do not include this bookmark
    mine = Playlist.objects.filter(user__id = user.id).exclude(bookmarks__pk = bookmark)
    # playlists I can edit that do not include this bookmark
    others = Playlist.objects.filter(editors__id = user.id).exclude(bookmarks__pk = bookmark)
    
    # playlists that already include this bookmark
    full_playlists = Playlist.objects.filter(bookmarks__pk = bookmark)
    
    return {'full_playlists': full_playlists, 
            'empty_playlists': list(chain(mine, others)), # to check if any playlists
            'empty_playlists_mine': mine,
            'empty_playlists_others': others, 
            'bm': bookmark}