from tastypie.validation import Validation, FormValidation
from bookmarks.models import PlaylistBookmarks, Vote

class CustomFormValidation(FormValidation):
    """ Overdide base FormValidation to pass request to form class 
    
        DO NOT PASS cleaned data back, other fields will be wiped 
    """
    def is_valid(self, bundle, request=None):
        data = bundle.data
        if data is None:
            data = {}
            
        ## patch for issue in tastypie - https://github.com/toastdriven/django-tastypie/issues/199
        if request.method == 'PUT' and 'id' in bundle.data:
            
            instance = bundle.obj.__class__.objects.get(pk=bundle.data['id'])
            form = self.form_class(data, instance=instance,request=request)
        else:
            form = self.form_class(data,request=request)

        if form.is_valid():
            return {}
        return form.errors

class PlaylistBookmarkValidation(Validation):
    def is_valid(self, bundle, request=None):
        
        bookmark_id = bundle.data['bookmark'].id
        playlist_id = bundle.data['playlist'].id
        
        objects = PlaylistBookmarks.objects.filter(bookmark__id=bookmark_id, playlist__id=playlist_id)
        if objects:
            return {'__all__':'This bookmark is already attached to this playlist'} 
        
        return {}


class VoteValidation(Validation):
    def is_valid(self, bundle, request=None):
        
        user = request.user
        object_id = bundle.data['object_id']
        content_type = bundle.data['content_type']
        content_type_id = content_type.id
        value = int(bundle.data.get("value", None))
        object = bundle.obj
        voting_on = content_type.get_object_for_this_type(id=object_id)

        if voting_on.user == request.user:  
            return {"__all__":"Sorry, you can't vote on your own item!"}

        if bundle.data['id'] != None:
            votes = Vote.objects.filter(user=user,object_id=object_id,content_type__id=content_type_id).exclude(id=bundle.data['id'])
        else:
            votes = Vote.objects.filter(user=user,object_id=object_id,content_type__id=content_type_id)
        
        if votes:
            return {"__all__":"You have already voted on this item, please delete your vote and post again."}
        
        if value not in [-1, 1]:
            return {"__all__":"Vote value must either be 1 or -1."}
            
        return {}
    
from tastypie.authorization import Authorization

class UserAuthorization(Authorization):
    """ Anyone can read data / Only user can affect data """
    def apply_limits(self, request, object_list):
        if request and hasattr(request, 'user'):
            if request.method == 'GET':
                object_list = object_list.filter()
            elif request.method in ['POST','PUT','DELETE']:
                object_list = object_list.filter(user=request.user)
            else:
                object_list = object_list.none()
        return object_list


class PlaylistBookmarUserAuthorization(Authorization):
    """ Anyone can read / Only user/editor or creator can post """    
    
    def is_authorized(self, request, object=None):
        if request.method == 'GET':
            return True
        else:
            if object:
                if request.user == object.user or request.user.id in object.editors.all().values_list('id', flat=True):
                    return True
            
            return False
