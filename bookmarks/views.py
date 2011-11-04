import django.http as http
import django.shortcuts as shortcuts
import django.template.context as context
from tagging.models import Tag, TaggedItem 
from django.core.urlresolvers import reverse
from models import Bookmark, Playlist, PlaylistBookmarks, Author, License, Vote
from django.db.models import Sum, Count, Max, Avg, Q
from django.db import models
from django.contrib import messages
from forms import AddAuthor
from django.utils.html import escape

def index(request):
    bag = {}
    bag['bookmarks'] = Bookmark.objects.all().order_by('-created')[:50]
    
    bag['playlists'] = Playlist.objects.all().order_by('-created')[:50]
    
    return shortcuts.render_to_response("index.html", 
                                        bag, 
                                        context_instance=context.RequestContext(request))


def test(request):
    bag = {}

    playlists = Playlist.objects.all()
    unique_bookmarks = Bookmark.objects.get_unique_by_score()
    unique_bookmark = Bookmark.objects.get_unique_url_by_score(url='http://www.oerglue.com/')
    bookmarks_by_url = Bookmark.objects.get_url_by_score(url='http://www.oerglue.com/')

    if request.user.is_authenticated():
        user = request.user
        user_bookmarks = Bookmark.objects.values_list('url', flat=True).filter(user=user)
        mutual_bookmarks = Bookmark.objects.values('user__username') \
                            .filter(url__in=user_bookmarks) \
                            .exclude(user=user) \
                            .annotate(num_mutual_bookmarks=Count('user')) \
                            .order_by('-num_mutual_bookmarks')
        bag['mutual_bookmarks'] = mutual_bookmarks
    bag['playlists'] = playlists
    bag['unique_bookmarks'] = unique_bookmarks
    bag['unique_bookmark'] = unique_bookmark
    bag['bookmarks_by_url'] = bookmarks_by_url

    return shortcuts.render_to_response("test.html", 
                                        bag, 
                                        context_instance=context.RequestContext(request))

def tags(request, tag = None):
    """Shows a list of all bookmarks containing a particular tag"""
    if tag is None:
        bookmarks = Bookmark.objects.all().distinct('url').order_by('-created')

    else:
        this_tag = Tag.objects.get(name=tag)
        bookmarks = TaggedItem.objects.get_by_model(Bookmark, this_tag).order_by('-created')
    return shortcuts.render_to_response("tag.html", 
                                        {'bookmarks': bookmarks, 
                                         'tag': tag}, 
                                        context_instance=context.RequestContext(request))

def comment_posted(request):
    """
    Hacked into django.contrib.comments to remove the quite frankly f*cking 
    ugly 'thanks' and error pages, and to use django.contrib.messages instead.
    """
    referer = request.META['HTTP_REFERER']
    if request.POST['comment'].strip(' ') == '':
        messages.error(request, "Your comment wasn't saved because it was blank.  Please add some text and try again.")
        return http.HttpResponseRedirect(referer)
    else:
        from django.contrib.comments.views.comments import post_comment
        post_comment(request, next=referer)
        messages.success(request, 'Thanks for your comment')
        return http.HttpResponseRedirect(referer)

def add_author(request):
    bag = {}
    if request.method == 'POST':
        form = AddAuthor(request.POST)
        if form.is_valid():
            object = form.save()
            return http.HttpResponse('valid||%s||%s' % (escape(object._get_pk_val()),escape(object)))
    else:
        form = AddAuthor()

    
    bag['form'] = form
    return shortcuts.render_to_response("lookup/add_author.html", 
                                    bag, 
                                    context_instance=context.RequestContext(request))

def close_iframe(request):
    """
    Closes the iframe and says thanks
    """
    
    return shortcuts.render_to_response("close_iframe.html", 
                                    context_instance=context.RequestContext(request))
