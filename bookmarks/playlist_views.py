import django.http as http
import django.shortcuts as shortcuts
import django.template.context as context
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from models import Playlist, PlaylistBookmarks, Bookmark
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from forms import AddPlaylist, EditPlaylist
from django.template.defaultfilters import slugify
import datetime

def index(request, username):
    bag = {}
    user = shortcuts.get_object_or_404(User, username=username)
    playlists = Playlist.objects.get_by_user(user.id)
    other_playlists = request.user.following_playlists.filter() | request.user.playlist_editor.filter()
    
    bag['playlists'] = playlists
    bag['other_playlists'] = other_playlists
    bag['user'] = user
    return shortcuts.render_to_response("playlist/index.html", 
                                        bag, 
                                        context_instance=context.RequestContext(request))

def view(request, username, slug):
    bag = {}
    user = shortcuts.get_object_or_404(User, username=username)
    playlist = shortcuts.get_object_or_404(Playlist, slug=slug, user=user)
    content_type = ContentType.objects.get_for_model(Playlist)

    bag['playlist'] = playlist
    bag['content_type'] = content_type
    
    return shortcuts.render_to_response("playlist/view.html", 
                                        bag, 
                                        context_instance=context.RequestContext(request))

@login_required
def add(request, username):
    bag = {}
    if request.method == 'POST':
        form = AddPlaylist(request.POST, request=request)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.user = request.user
            playlist.slug = slugify(form.cleaned_data['title'])
            playlist.save()

            Playlist.objects.save_bookmarks(playlist, form.cleaned_data['bookmarks'])                

            messages.info(request, 'Playlist %s added.' % playlist)
            
            return http.HttpResponseRedirect(reverse('bookmarks.playlist_views.view', args=[playlist.user.username,playlist.slug,]))
    else:
        form = AddPlaylist(request=request)
            
    bag['form'] = form

    return shortcuts.render_to_response("playlist/add.html", 
                                        bag, 
                                        context_instance=context.RequestContext(request))

@login_required
def edit(request, username, slug):
    bag = {}
    user = shortcuts.get_object_or_404(User, username=username)
    playlist = shortcuts.get_object_or_404(Playlist, slug=slug, user=user)
    
    ## if not creator then check if editor, else raise 404
    try:
        if request.user.id != playlist.user.id:
            is_editor = playlist.editors.get(id=request.user.id)
    except:
        raise http.Http404
    
    if request.method == 'POST':
        form = EditPlaylist(request.POST, request=request, instance=playlist)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.save()
            
            Playlist.objects.save_bookmarks(playlist, form.cleaned_data['bookmarks'])   
            
            if form.cleaned_data.get('editors',None):               
                Playlist.objects.save_editors(playlist, form.cleaned_data['editors'])
       
            messages.info(request, 'Playlist %s edited.' % playlist)
            
            return http.HttpResponseRedirect(reverse('bookmarks.playlist_views.view', args=[playlist.user.username,playlist.slug,]))
    else:
        form = EditPlaylist(request=request, instance=playlist)
            
    bag['form'] = form

    return shortcuts.render_to_response("playlist/edit.html", 
                                        bag, 
                                        context_instance=context.RequestContext(request))

@login_required
def follow(request, username, slug):
    """ Add current user as a 'follower' for this playlist """
    
    user = shortcuts.get_object_or_404(User, username=username)
    playlist = shortcuts.get_object_or_404(Playlist, slug=slug, user=user)
    playlist.followers.add(request.user)
    messages.info(request, 'You are now following %s' % playlist)
    
    return http.HttpResponseRedirect(reverse('bookmarks.playlist_views.view', args=[playlist.user.username,playlist.slug,]))


@login_required
def unfollow(request, username, slug):
    """ remove current user as a 'follower' for this playlist """
    
    user = shortcuts.get_object_or_404(User, username=username)
    playlist = shortcuts.get_object_or_404(Playlist, slug=slug, user=user)
    playlist.followers.remove(request.user)
    messages.info(request, 'You are no longer following %s' % playlist)
    
    return http.HttpResponseRedirect(reverse('bookmarks.playlist_views.view', args=[playlist.user.username,playlist.slug,]))

@login_required
def fork(request, username, slug):
    """ creates new for of playlist, with parent set as current playlist 
    
        Does not copy editors, followers or votes
    
    """
    parent_owner = shortcuts.get_object_or_404(User, username=username)
    parent_playlist = shortcuts.get_object_or_404(Playlist, slug=slug, user=parent_owner)

    # create new fork
    new_playlist = Playlist(use=request.user, 
                            title = parent_playlist.title,
                            slug = parent_playlist.slug,
                            parent_fork=parent_playlist)
    new_playlist.save()    
    
    Playlist.objects.save_bookmarks(new_playlist, parent_playlist.bookmarks.values_list('id'))
                 
    messages.info(request, 'Playlist forked - You are now viewing your fork')
    
    return http.HttpResponseRedirect(reverse('bookmarks.playlist_views.view', args=[new_playlist.user.username,new_playlist.slug,]))


@login_required
def add_to_playlist(request):
    if request.method != 'POST':
        raise Http404()
    
    bookmark = shortcuts.get_object_or_404(Bookmark, pk = request.POST['bookmark'])
    playlist = shortcuts.get_object_or_404(Playlist, pk = request.POST['playlist'])
    
    # need to check I have write access
    write_access = False
    if playlist.user == request.user:
        write_access = True
    else:
        try:
            pl = playlist.editors.get(id = request.user.id)
            write_access = True
        except:
            messages.error(request, 'You do not have permission to add records to the "%s" playlist' %(playlist.title))
    
    if write_access is True:
        pb = PlaylistBookmarks(bookmark = bookmark, 
                               playlist = playlist)
        pb.save()
        messages.success(request, 'This bookmark has been added to  the "%s" playlist' %(playlist.title))
    
    return http.HttpResponseRedirect(reverse('bookmarks.bookmark_views.view', args=[bookmark.user.username,bookmark.slug,]))
    