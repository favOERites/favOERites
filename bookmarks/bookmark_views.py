import django.http as http
import django.shortcuts as shortcuts
import django.template.context as context
from django.core.urlresolvers import reverse
from models import Bookmark, Playlist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from forms import AddBookmark, EditBookmark
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify
from tagging.models import Tag, TaggedItem
from django.db import models

def index(request, username):
    bag = {}
    user = shortcuts.get_object_or_404(User, username=username)
    bookmarks = Bookmark.objects.get_by_user(user.id)
    bag['bookmarks'] = bookmarks
    bag['user'] = user
    return shortcuts.render_to_response("bookmark/index.html", 
                                        bag, 
                                        context_instance=context.RequestContext(request))

def view(request, username, slug):
    bag = {}    
    user = shortcuts.get_object_or_404(User, username=username)
    bookmark = shortcuts.get_object_or_404(Bookmark, user=user, slug=slug)
    content_type = ContentType.objects.get_for_model(Bookmark)
    bag['bookmark'] = bookmark
    bag['content_type'] = content_type
    bag['username'] = username
    return shortcuts.render_to_response("bookmark/view.html", 
                                        bag, 
                                        context_instance=context.RequestContext(request))

@login_required     
def add(request, username):
    bag = {}
    if request.method == 'POST':
        form = AddBookmark(request.POST,request=request)
        if form.is_valid():
            bookmark = form.save(commit=False)
            bookmark.user = request.user
            bookmark.slug = slugify(form.cleaned_data['title'])
            bookmark.save()
            form.save_m2m()
            messages.info(request, 'Bookmark %s added.' % bookmark)
            return http.HttpResponseRedirect(reverse('bookmarks.bookmark_views.view', args=[bookmark.user.username,bookmark.slug,]))
    else:
        form = AddBookmark(request=request)
            
    bag['form'] = form

    return shortcuts.render_to_response("bookmark/add.html", 
                                        bag, 
                                        context_instance=context.RequestContext(request))

    
@login_required
def edit(request, username, slug):
    bag = {}
    bookmark = shortcuts.get_object_or_404(Bookmark, user=request.user, slug=slug)
    if request.method == 'POST':
        form = EditBookmark(request.POST, instance=bookmark)
        if form.is_valid():
            bookmark = form.save(commit=False)
            bookmark.user = request.user
            bookmark.save()
            form.save_m2m()
            messages.info(request, 'Bookmark %s edited.' % bookmark)
            return http.HttpResponseRedirect(reverse('bookmarks.bookmark_views.view', args=[bookmark.user.username,bookmark.slug,]))
    else:
        form = EditBookmark(instance=bookmark)
            
    bag['form'] = form

    return shortcuts.render_to_response("bookmark/edit.html", 
                                        bag, 
                                        context_instance=context.RequestContext(request))

def tags(request, tag = None):
    """Shows a list of all bookmarks containing a particular tag"""
    if tag is None:
        bookmarks = Bookmark.objects.all().distinct('url').order_by('-created')    
    else:
        this_tag = Tag.objects.get(name=tag)
        bookmarks = TaggedItem.objects.get_by_model(Bookmark, this_tag)

    return shortcuts.render_to_response("tag.html",
                                        {'bookmarks': bookmarks,
                                        'tag': tag},
                                        context_instance=context.RequestContext(request))



def add_bookmark(request):
    """
    Add bookmark bookmarklet
    """
    if request.user.is_authenticated():
        bag = {}
        if request.method == 'POST':
            form = AddBookmark(request.POST,request=request)
            if form.is_valid():
                bookmark = form.save(commit=False)
                bookmark.user = request.user
                bookmark.slug = slugify(form.cleaned_data['title'])
                bookmark.save()
                messages.info(request, 'Bookmark %s added.' % bookmark)
                return http.HttpResponseRedirect('/close_iframe/')
        else:
            try: title = request.GET['title']
            except: title = ''
            try: url = request.GET['url']
            except: url = ''
            try: 
                licence_url = request.GET['licence']
                
                try: 
                    licence = Licence.objects.get(url = license_url)
                except:
                    #licence_title = request.GET['license_title'] 
                    licence = Licence(url = licence_url, type = licence_url)
                    licence.save()
                
            except: 
                licence = ''
                licence_url = ''
                
            try: description = request.GET['description']
            except: description = ''
            form = AddBookmark(request=request, initial = {'title': title, 'url': url, 'licences': licence, 'description': description})
            bag['licence'] = licence_url
        bag['form'] = form
    
        return shortcuts.render_to_response("bookmark/add_small.html", 
                                            bag, 
                                            context_instance=context.RequestContext(request))


    else:
        return http.HttpResponseRedirect('/auth/login-popup/')