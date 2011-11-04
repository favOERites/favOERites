from django.db import models
from django.contrib.auth.models import User
from tagging.fields import TagField
from tagging.models import Tag
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models import Sum, Count, Max
import models as bookmark_models
import itertools


class BookmarkManager(models.Manager):
    
    def get_unique_by_score(self,user_id=None):
        """ get list of unique bookmarks, based on url ordered by score. 
            Note returns list not queryset, values need to be after annote for group by to work
            values are listed, if not then not foreign key values are returned. e.g user__username
            """
            
        if user_id:
            bookmarks = bookmark_models.Bookmark.objects.filter(user__id=user_id).annotate(score=Sum('votes__value')).values('user__username','score','url','slug','title').order_by('-score')
        else:
            bookmarks = bookmark_models.Bookmark.objects.annotate(score=Sum('votes__value')).values('user__username','score','url','slug','title').order_by('-score')
        unique_bookmarks = []

        # remove duplicates
        for bookmark in bookmarks:
            if bookmark['url'] not in [ub['url'] for ub in unique_bookmarks]:
                unique_bookmarks.append(bookmark)

        return unique_bookmarks
    
    def get_by_url(self, url):
        """ get all instances of Bookmark by a url """
        return bookmark_models.Bookmark.objects.filter(url=url)
    
    def get_related_by_url(self, obj):
        """ get all Bookmark instances related by url to obj """
        return self.get_by_url(obj.url).exclude(id=obj.id)
    
    def get_url_by_score(self, url):
        """ get the Bookmarks matching url"""
        return bookmark_models.Bookmark.objects.filter(url=url).annotate(score=Sum('votes__value')).order_by('-score')
    
    def get_unique_url_by_score(self, url):
        """ get the Bookmark matching url with the highest score """
        bookmarks = self.get_url_by_score(url)
        if bookmarks:
            return bookmarks[0]
        else:
            return None

    def get_by_user(self, user_id):
        """ get all instances of Bookmark by a url """
        return bookmark_models.Bookmark.objects.filter(user__id=user_id)

    def get_user_score(self, user):
        return sum(b.score for b in bookmark_models.Bookmark.objects.filter(user=user).annotate(score=Sum('votes__value')).order_by('-score') if b.score)

  
class PlaylistManager(models.Manager):
    def get_by_user(self, user_id):
        """ get all instances of Playlist by a url """
        return bookmark_models.Playlist.objects.filter(user__id=user_id)
    
    def save_bookmarks(self, obj, bookmark_ids):
        old_bookmark_ids = obj.bookmarks.all().values_list('id', flat=True)
        new_bookmark_ids = []
        
        # create link if doesnt exits
        bookmarks = bookmark_models.Bookmark.objects.filter(id__in=bookmark_ids)
        for bookmark in bookmarks:
            new_bookmark_ids.append(bookmark.id)
            if bookmark.id not in old_bookmark_ids:     
                bookmark_models.PlaylistBookmarks.objects.create(bookmark=bookmark, playlist=obj)               
        
        # compare old and new, delete if  
        for id in old_bookmark_ids:
            if id not in new_bookmark_ids:
                bookmark_models.PlaylistBookmarks.objects.get(playlist__id=obj.id, bookmark__id=id).delete()
    
    def save_editors(self, obj, editor_ids):
        old_editor_ids = obj.editors.all().values_list('id', flat=True)
        new_editor_ids = []
        
        # create link if doesnt exits
        editors = User.objects.filter(id__in=editor_ids)
        for editor in editors:
            new_editor_ids.append(editor.id)
            if editor.id not in old_editor_ids:     
                obj.editors.add(editor)            
        
        # compare old and new, delete if  
        for id in old_editor_ids:
            if id not in new_editor_ids:
                obj.editors.delete(editor)         
    
    def get_by_score(self):
        return bookmark_models.Playlist.objects.annotate(score=Sum('votes__value')).order_by('-score')
    
    def get_by_followers(self):
        return bookmark_models.Playlist.objects.annotate(num=Count('followers')).order_by('-num')

    def get_user_score(self, user):
        return sum(p.score for p in bookmark_models.Playlist.objects.filter(user=user).annotate(score=Sum('votes__value')).order_by('-score') if p.score)

class VoteManager(models.Manager):
    def add_vote(self, obj, value, user):
        """ Associates vote with object """
        contenttype = ContentType.objects.get_for_model(obj)
       
        # create or update - note value exclude 
        obj, created = bookmark_models.Vote.objects.get_or_create(content_type=contenttype,object_id=obj.id, user=user)
        obj.value = value
        obj.save()

    def get_all_for_object(self, obj):
        contenttype = ContentType.objects.get_for_model(obj)
        return self.filter(content_type__id=contenttype.id,object_id=obj.id)
            
    def get_score_for_object(self, obj):
        contenttype = ContentType.objects.get_for_model(obj)
        return self.filter(content_type__id=contenttype.id,object_id=obj.id).aggregate(score=Sum('value'))['score']

    def get_up_for_object(self, obj):
        contenttype = ContentType.objects.get_for_model(obj)
        return self.filter(content_type__id=contenttype.id,object_id=obj.id, value=1).aggregate(score=Sum('value'))['score']

    def get_down_for_object(self, obj):
        contenttype = ContentType.objects.get_for_model(obj)
        return self.filter(content_type__id=contenttype.id,object_id=obj.id, value=-1).aggregate(score=Sum('value'))['score']
    
    def get_user_vote(self, user, obj):
        contenttype = ContentType.objects.get_for_model(obj)
        votes = self.filter(content_type__id=contenttype.id,object_id=obj.id, user__id=user.id)
        if votes:
            return votes[0]
        else:
            return None
        
        
    def get_users_by_score(self):
        users = User.objects.all()
        
        for user in users:
            bookmarks = Bookmark.objects.get_user_score(user)
            playlists = Playlist.objects.get_user_score(user)
            user.total_score = bookmarks + playlists
            
        return users[0].total_score
