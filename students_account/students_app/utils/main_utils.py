from django.http import HttpResponseRedirect

def is_authenticated(func):
    def wrapper(request, *args, ** kwargs):
        if request.user.is_authenticated():
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('../index')
    return wrapper

def class_for_name(name, namespace=None):
    if not namespace:
        attrs = name.split('.')
    else:
        attrs = '.'.join((namespace, name)).split('.')
    return reduce(getattr, attrs[1:], __import__(attrs[0]))

def table_to_class_name(table_name):
    namespace = 'students_account.students_app.models.'
    words = [w.title() for w in table_name.split('_')]
    return (namespace + ''.join(words))
