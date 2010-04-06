def settings_proc(request):
    from django.conf import settings
    return {'django_settings': settings}
