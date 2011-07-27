from django.conf import settings
from django.contrib import auth
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

def _get_next(request):
    """
    Returns a url to redirect to after the login
    """
    if 'next' in request.session:
        next = request.session['next']
        del request.session['next']
        return next
    elif 'next' in request.GET:
        return request.GET.get('next')
    elif 'next' in request.POST:
        return request.POST.get('next')
    else:
        return getattr(settings, 'LOGIN_REDIRECT_URL', '/')

def facebook_login(request, template='facebook_error.html'):
    if request.facebook is not None:
        user = auth.authenticate(fb_uid=request.facebook.uid, fb_object=request.facebook)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(_get_next(request))

    return HttpResponseRedirect('/')
