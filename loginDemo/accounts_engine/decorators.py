from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from accounts_engine.models import *
from accounts_engine.custom_processor import get_all_permitted_sections_and_urls


def is_user_allowed(function):
    def wrap(request, *args, **kwargs):
        permitted_sections_and_urls = get_all_permitted_sections_and_urls(request)
        if request.resolver_match.url_name in permitted_sections_and_urls['permitted_url_list']:
            return function(request, *args, **kwargs)
        else:
            return HttpResponse('you are trying to access a link or perform an action for which you do not have permission.<br> Please contact Admin if you think you should have access to this link or action. <br> please hit back to go back to previous page')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
