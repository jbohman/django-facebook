from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
import re

from models import FacebookProfile

FACEBOOK_PREPOPULATE_USER_DATA = getattr(settings, 'FACEBOOK_PREPOPULATE_USER_DATA', None)
FACEBOOK_EXTENDED_PERMISSIONS = getattr(settings, 'FACEBOOK_EXTENDED_PERMISSIONS', None)

class FacebookBackend(ModelBackend):
    """ Authenticate a facebook user. """
    def authenticate(self, fb_uid=None, fb_object=None):
        """ If we receive a facebook uid then the cookie has already been validated. """
        if fb_uid:
            user, created = User.objects.get_or_create(username=fb_uid)

            # Consider replacing this synchronous data request (out to Facebook
            # and back) with an asynchronous request, using Celery or similar tool
            if FACEBOOK_PREPOPULATE_USER_DATA and created and fb_object:
                fb_user = fb_object.graph.get_object(u'me')
                user.first_name = fb_user['first_name']
                user.last_name  = fb_user['last_name']

                if 'email' in FACEBOOK_EXTENDED_PERMISSIONS and 'email' in fb_user:
                    user.email = fb_user['email']
                    
                user.save()

                profile = FacebookProfile()

                profile.user = user

                if 'birthday' in fb_user:
                    match = re.search('(\d+)/(\d+)/(\d+)', fb_user['birthday'])
                    if match:
                        profile.birthday = "%s-%s-%s" % (match.group(3), match.group(1), match.group(2))

                profile.uid = fb_user['id']
                profile.name = fb_user['name']
                profile.first_name = fb_user['first_name']
                profile.middle_name = fb_user['middle_name']
                profile.last_name = fb_user['last_name']
                profile.link = fb_user['link']
                profile.hometown = fb_user['hometown']
                profile.bio = fb_user['bio']
                profile.gender = fb_user['gender']
                profile.modified = fb_user['updated_time'].replace('T', ' ').replace('+', '.')

                profile.save()

            return user
        return None
