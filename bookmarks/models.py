from django.db import models
from django.contrib.auth.models import User
from tagging.fields import TagField
from tagging.models import Tag
from tagging_autocomplete.models import TagAutocompleteField
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models import Sum
from django.db.models import Count
from managers import BookmarkManager, VoteManager, PlaylistManager
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.contrib.comments.models import Comment

     
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, related_name='profile')
    
    def total_score(self):
        user = self.user
        bookmarks = self.bookmarks_score()
        playlists = self.playlist_score()
        total_score = bookmarks + playlists
        return total_score
    
    def bookmarks_score(self):
        return Bookmark.objects.get_user_score(self.user)
    
    def playlist_score(self):
        return Playlist.objects.get_user_score(self.user)

class Author(models.Model):
    """
    Holds information about the author of a particular resource.  
    
    We have deliberately NOT linked this to a user record, as that would have 
    made the system extremely complicated
    """
    title = models.CharField(max_length=20)
    forenames = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    organisation = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s %s %s" % (self.title, self.forenames, self.surname)

class Bookmark(models.Model):
    """
    The Bookmark table is the main storage point for the resources.
        
    A bookmark's slug is unique with a user record, so it is perfectly OK to 
    have several bookmarks with the same slug - as long as they're owned by 
    different users.  Bookmarks are therefore always accessed through their 
    'owner'.  This forces the system to be used for personal collections of 
    resources rather than being 'just another repository'.   
    """
    title = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField()
    url = models.URLField()
    description = models.TextField(blank=True)
    keywords = TagAutocompleteField()
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    authors = models.ManyToManyField('Author', null=True, blank=True)
    licences = models.ManyToManyField('License', null=True, blank=True)
    publishers = models.ManyToManyField('Publisher', null=True, blank=True)
    
    user = models.ForeignKey(User, related_name='bookmarks')
   
    votes = generic.GenericRelation('Vote')
    
    objects = BookmarkManager()
    
    comments = generic.GenericRelation(Comment, object_id_field='object_pk')

    
    def __unicode__(self):
        return self.url
    
    def score(self):
        return Vote.objects.get_score_for_object(self)

    def up(self):
        return Vote.objects.get_up_for_object(self)

    def down(self):
        return Vote.objects.get_down_for_object(self)

    def get_absolute_url(self):
        return reverse('bookmarks.bookmark_views.view', args=[self.user.username,self.slug,])
    
    def _get_tags(self):
        return Tag.objects.get_for_object(self)
    
    def _set_tags(self, tag_list):
        Tag.objects.update_tags(self, tag_list)    
    tags = property(_get_tags, _set_tags)
    
    def save(self, *args, **kwargs):
        """
        When you save a bookmark it automatically sets the modified date.
 
        If it's the first time you save it it also sets a default record in the 
        Votes table.  The default value in votes means that it always has a score.
        """
        if not self.slug:
            self.slug = slugify(self.title)

        self.modified = datetime.now()
        super(Bookmark, self).save(*args, **kwargs)
        
        if not self.votes.all():
            Vote.objects.add_vote(self, 0, self.user)

    class Meta:
        unique_together = ("slug", "user")

class License(models.Model):
    """
    We have chosen to keep licence information as simple as possible.  So we 
    only need a url and the 'type' of licence (i.e. it's name).  We may choose 
    to expand on this later, but it is probably outside of the scope of this 
    initial project.
    """
    type = models.CharField(max_length=255)
    url = models.URLField()
    
    def __unicode__(self):
        return self.type

class Playlist(models.Model):
    """
    Playlists are user-owned collections of bookmarks.  These are tagged, and 
    can be shared with other users.
    
    By default Playlists are publicly readable, but the author can choose other 
    users who can modify them (editors).
    
    If you like a Playlist you can follow it to see changes that have been made.  
    You can also 'fork' a playlist to create a cloned version of it.  We are 
    also going to have the option to merge back in a forked playlist.
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    bookmarks = models.ManyToManyField('Bookmark', through='PlaylistBookmarks')
       
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    user = models.ForeignKey(User, related_name='playlists')
    followers =  models.ManyToManyField(User, null=True, blank=True, related_name='following_playlists')
    editors =  models.ManyToManyField(User, null=True, blank=True, related_name='playlist_editor')
    parent_fork = models.ForeignKey('Playlist', null=True, blank=True)

    votes = generic.GenericRelation('Vote')

    objects = PlaylistManager()

    comments = generic.GenericRelation(Comment, object_id_field='object_pk')

    def __unicode__(self):
        return self.title
    
    def number_of_bookmarks(self):
        return self.bookmarks.all().count()
    
    def number_of_followers(self):
        return self.followers.all().count()

    def score(self):
        return Vote.objects.get_score_for_object(self)

    def up(self):
        return Vote.objects.get_up_for_object(self)

    def down(self):
        return Vote.objects.get_down_for_object(self)

    def get_absolute_url(self):
        return reverse('bookmarks.playlist_views.view', args=[self.user.username,self.slug,])

    def forked_from(self):
        """
        Returns a blank string if it hasn't been forked
        """
        if self.parent_fork:
            return self.parent_fork
        else:
            return ""

    def save(self, *args, **kwargs):
        """
        When you save a playlist it automatically sets the modified date.
        
        If it's the first time you save it it also sets a default record in the 
        Votes table.  The default value in votes means that it always has a score.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        
        self.modified = datetime.now()
        super(Playlist, self).save(*args, **kwargs)
        
        if not self.votes.all():
            Vote.objects.add_vote(self, 0, self.user)

    class Meta:
        unique_together = ("slug", "user")

class PlaylistBookmarks(models.Model):
    """
    This is a simple link table to show which bookmarks are in which playlists
    """
    bookmark = models.ForeignKey('bookmark')
    playlist = models.ForeignKey('playlist')
    order = models.IntegerField(default=0)
    alt_title = models.CharField(max_length=255,null=True, blank=True)
    
    def __unicode__(self):
        return "%s : %s" % (self.bookmark, self.playlist)
    
    class Meta:
        ordering = ['-order', '-id']

class Publisher(models.Model):
    """
    Publisher information has deliberately been kept simple.  This may need 
    changing because it is possible that it could require a lot of additional 
    information such as address, contact details etc.  But that might be 
    another one for after the project!
    """
    title = models.CharField(max_length=20)
    forenames = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    organisation = models.CharField(max_length=255)
    
    def __unicode__(self):
        return "%s %s %" % (self.title, self.forenames, self.surname)

class Vote(models.Model):
    """
    Bookmarks (and Playlists) are rated on a simple vote up/vote down system.  
    This table records those votes (+1, -1).  When a new record gets added a 
    record is also added here with a value of 0.
    """
    value = models.IntegerField(null=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    voted_object = generic.GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(User)

    objects = VoteManager()    
    
    def __unicode__(self):
        return "%s for %s" % (self.value, self.voted_object)
    
    class Meta:
        unique_together = ("content_type", "object_id", "user")