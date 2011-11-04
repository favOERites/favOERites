import settings
from django import template
from django.template.defaultfilters import truncatewords, truncatewords_html, safe, linebreaks, striptags
from django.contrib.contenttypes.models import ContentType
from bookmarks.models import Vote
from django.core.urlresolvers import reverse

register = template.Library()

@register.filter
def get_user_vote(user, object):
    vote = Vote.objects.get_user_vote(user,object)
    if vote:
        return vote.value
    else:
        return None


@register.inclusion_tag('vote/vote.html')
def vote_on_object(request, object):
    content_type = ContentType.objects.get_for_model(object)
    if hasattr(object, 'user'): 
        owner =     getattr(object,'user') 
    else:
        owner = None 
     
    return {'request': request, 'object':object, 'content_type':content_type,'owner':owner}


@register.inclusion_tag('vote/vote_inline.html')
def vote_on_object_inline(request, object):
    content_type = ContentType.objects.get_for_model(object)
    if hasattr(object, 'user'): 
        owner =     getattr(object,'user') 
    else:
        owner = None 
     
    return {'request': request, 'object':object, 'content_type':content_type,'owner':owner}