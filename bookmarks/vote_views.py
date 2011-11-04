import django.http as http
import django.shortcuts as shortcuts
import django.template.context as context
from django.core.urlresolvers import reverse
from models import Vote
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages


@login_required
def vote(request, vote, object_id, content_type_id):
    vote = int(vote)
    if vote not in [-1,1]:
        raise http.Http404

    content_type = shortcuts.get_object_or_404(ContentType, id=content_type_id)
    object = shortcuts.get_object_or_404(content_type.model_class(), id=object_id)
    vote = Vote.objects.add_vote(object,vote,request.user)
    
    messages.info(request, 'Voted on %s' % (object))

    return http.HttpResponseRedirect(object.get_absolute_url())

