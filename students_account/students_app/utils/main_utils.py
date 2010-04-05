from django.http import HttpResponseRedirect

def is_authenticated(func):
    def wrapper(request, *args, ** kwargs):
        if request.user.is_authenticated():
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('../index')
    return wrapper
