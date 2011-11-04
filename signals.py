from django.contrib.auth.models import User
from django.db import models
from tastypie.models import create_api_key
from django.db.models.signals import post_save

## Create UserProfile
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

## Create API key
post_save.connect(create_api_key, sender=User)
