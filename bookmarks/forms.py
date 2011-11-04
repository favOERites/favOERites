from django import forms
import models
from django.contrib.auth.models import User
from ajax_select.fields import AutoCompleteSelectMultipleField, AutoCompleteSelectField
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

class AddBookmark(forms.ModelForm):
    authors = AutoCompleteSelectMultipleField('author', required=False)
    licences = AutoCompleteSelectMultipleField('license', required=False)
    class Meta:
        model = models.Bookmark
        fields = ('title', 'url', 'description', 'keywords', 'authors', 'licences')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AddBookmark, self).__init__(*args, **kwargs)
        
        # add link
        self.fields['authors'].widget.add_link = reverse('bookmarks.views.add_author')

    def clean(self):
        cleaned_data = self.cleaned_data
        user = self.request.user
        title = cleaned_data.get("title")
        slug = slugify(title)
        
        if self.instance:
            bookmarks = models.Bookmark.objects.filter(user=user,slug=slug).exclude(id=self.instance.id)
        else:
            bookmarks = models.Bookmark.objects.filter(user=user,slug=slug)
            
        if bookmarks:
            raise forms.ValidationError("Your have already used this title, please choose again.")
            ## slug should not be returned in cleaned_data, create in model save() so it works for API 
            
        return cleaned_data
    
class EditBookmark(forms.ModelForm):
    authors = AutoCompleteSelectMultipleField('author', required=False)
    licences = AutoCompleteSelectMultipleField('license', required=False)

    class Meta:
        model = models.Bookmark
        fields = ('title', 'url', 'description', 'keywords', 'authors', 'licences')
 
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(EditBookmark, self).__init__(*args, **kwargs)
        
        self.fields['authors'].initial = [a.id for a in self.instance.authors.all()]
        self.fields['licences'].initial = self.instance.licences.all()

        # add link
        self.fields['authors'].widget.add_link = reverse('bookmarks.views.add_author')


class AddPlaylist(forms.ModelForm):
    class Meta:
        model = models.Playlist
        fields = ('title', 'bookmarks',)

    def __init__(self, *args, **kwargs):  
        self.request = kwargs.pop('request', None)     
        super(AddPlaylist, self).__init__(*args, **kwargs)  
          
        self.fields["bookmarks"] = AutoCompleteSelectMultipleField('bookmarks', required=False)
        self.fields["bookmarks"].help_text = 'Start typing the name or URL of the bookmark you wish to add, a list will be displayed for you to select from.'  

    
    def clean(self):
        cleaned_data = self.cleaned_data
    
        user = self.request.user
        title = cleaned_data.get("title")
        slug = slugify(title)
        if self.instance:
            playlists = models.Playlist.objects.filter(user=user,slug=slug).exclude(id=self.instance.id)
        else:
            playlists = models.Playlist.objects.filter(user=user,slug=slug)
            
        if playlists:
            raise forms.ValidationError("Your have already used this title, please choose again.")
           
        return cleaned_data


class EditPlaylist(forms.ModelForm):
    class Meta:
        model = models.Playlist
        fields = ('title', 'bookmarks', 'editors')
        
    def __init__(self, *args, **kwargs):  
        self.request = kwargs.pop('request', None)         
        super(EditPlaylist, self).__init__(*args, **kwargs)  
        self.fields["bookmarks"] = AutoCompleteSelectMultipleField('bookmarks', required=False)
        self.fields["bookmarks"].help_text = 'Start typing the name or URL of the bookmark you wish to add, a list will be displayed for you to select from.'  
        
        self.fields["editors"] = AutoCompleteSelectMultipleField('non_staff_users', required=False)
        self.fields["editors"].help_text = 'Start typing the usenrame editor you wish to add, a list will be displayed for you to select from.'

        # if not owner remove editor input
        if self.request.user.id != self.instance.user.id:
            del self.fields['editors']
        
class AddAuthor(forms.ModelForm):
    class Meta:
        model = models.Author


class AddVote(forms.ModelForm):
    """ Only for API """
    class Meta:
        model = models.Vote
        fields = ('value','content_type', 'object_id')

    def __init__(self, *args, **kwargs):  
        self.request = kwargs.pop('request', None)     
        super(AddVote, self).__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        user = self.request.user
        value = cleaned_data.get("value")
        object_id = cleaned_data.get("object_id")
        content_type = cleaned_data.get("content_type")
  
        if self.instance:           
            votes = models.Vote.objects.filter(user=user,object_id=object_id,content_type__id=content_type.id).exclude(id=self.instance.id)
        else:
            votes = models.Vote.objects.filter(user=user,object_id=object_id,content_type__id=content_type.id)
        
        if votes:
            raise forms.ValidationError("You have already voted on this item, please delete your vote and post again.")
        
        if value not in [-1, 1]:
            raise forms.ValidationError("Vote value must either be 1 or -1.")
            
        return cleaned_data

    