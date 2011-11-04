import models 
from django.db.models import Q
from django.contrib.auth.models import User

class AuthorLookup(object):

    def get_query(self,q,request):
        """ return a query set.  you also have access to request.user if needed """
        return models.Author.objects.filter(Q(forenames__istartswith=q) | Q(surname__istartswith=q))

    def format_result(self,author):
        """ the search results display in the dropdown menu.  may contain html and multiple-lines. will remove any |  """
        return unicode(author)

    def format_item(self,author):
        """ the display of a currently selected object in the area below the search box. html is OK """
        return unicode(author)

    def get_objects(self,ids):
        """ given a list of ids, return the objects ordered as you would like them on the admin page.
            this is for displaying the currently selected items (in the case of a ManyToMany field)
        """
        return models.Author.objects.filter(pk__in=ids).order_by('forenames','surname')
    
    
class LicenseLookup(object):

    def get_query(self,q,request):
        """ return a query set.  you also have access to request.user if needed """
        return models.License.objects.filter(type__istartswith=q)

    def format_result(self,license):
        """ the search results display in the dropdown menu.  may contain html and multiple-lines. will remove any |  """
        return unicode(license)

    def format_item(self,license):
        """ the display of a currently selected object in the area below the search box. html is OK """
        return unicode(license)

    def get_objects(self,ids):
        """ given a list of ids, return the objects ordered as you would like them on the admin page.
            this is for displaying the currently selected items (in the case of a ManyToMany field)
        """
        return models.License.objects.filter(pk__in=ids).order_by('type')
    
        
class UserLookup(object):

    def get_query(self,q,request):
        """ return a query set.  you also have access to request.user if needed """
        return User.objects.filter(username__istartswith=q, is_staff=False)

    def format_result(self,user):
        """ the search results display in the dropdown menu.  may contain html and multiple-lines. will remove any |  """
        return unicode(user)

    def format_item(self,user):
        """ the display of a currently selected object in the area below the search box. html is OK """
        return unicode(user)

    def get_objects(self,ids):
        """ given a list of ids, return the objects ordered as you would like them on the admin page.
            this is for displaying the currently selected items (in the case of a ManyToMany field)
        """
        return User.objects.filter(pk__in=ids).order_by('username')
    
    
class BookmarkLookup(object):

    def get_query(self,q,request):
        """ return a query set.  you also have access to request.user if needed """
        return models.Bookmark.objects.filter(Q(title__istartswith=q)|Q(url__istartswith=q))

    def format_result(self,bookmark):
        """ the search results display in the dropdown menu.  may contain html and multiple-lines. will remove any |  """
        return "%s - %s" % (bookmark.title, bookmark.url)

    def format_item(self,bookmark):
        """ the display of a currently selected object in the area below the search box. html is OK """
        return "%s - %s" % (bookmark.title, bookmark.url)

    def get_objects(self,ids):
        """ given a list of ids, return the objects ordered as you would like them on the admin page.
            this is for displaying the currently selected items (in the case of a ManyToMany field)
        """
        return models.Bookmark.objects.filter(pk__in=ids).order_by('title')