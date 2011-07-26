from django import template
from django.conf import settings

register = template.Library()

FACEBOOK_EXTENDED_PERMISSIONS = getattr(settings, 'FACEBOOK_EXTENDED_PERMISSIONS', [])

@register.inclusion_tag('tags/facebook_js.html')
def facebook_js():
    app_id = getattr(settings, 'FACEBOOK_APP_ID', None)
    api_key = getattr(settings, 'FACEBOOK_API_KEY', None)
    perms = ','.join(FACEBOOK_EXTENDED_PERMISSIONS)
    return {'facebook_app_id': app_id, 'facebook_api_key': api_key, 'facebook_req_perms': perms}

@register.inclusion_tag('tags/facebook_button.html', takes_context=True)
def facebook_button(context, button=None):
    if not 'request' in context:
        raise AttributeError, 'Please add the ``django.core.context_processors.request`` context processors to your settings.TEMPLATE_CONTEXT_PROCESSORS set'
    logged_in = context['request'].user.is_authenticated()
    if 'next' in context:
        next = context['next']
    else:
        next = None
    return dict(next=next, logged_in=logged_in, button=button, request=context['request'])

@register.simple_tag
def facebook_perms():
    return ",".join(FACEBOOK_EXTENDED_PERMISSIONS)
