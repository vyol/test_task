# Create your views here.
import logging
import students_app.grids
from django.contrib import auth
from django.forms.util import ValidationError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.db.models import Count
from django.shortcuts import render_to_response
from django.template import RequestContext
from students_app.context_processors import settings_proc
from students_app.models import Grup, Student
from students_app.utils.main_utils import is_authenticated, class_for_name

DEFAULT_START_PAGE = '../groups'
ERROR_MESSAGE = "Please enter a correct username and password"


def login(request):
    if not request.POST:
        return display_login_form(request)
    if not request.session.test_cookie_worked():
        message = """Looks like your browser isn't configured to accept cookies.
                  Please enable cookies, reload this page, and try again."""
        return display_login_form(request, message)
    else:
        request.session.delete_test_cookie()
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect(DEFAULT_START_PAGE)
    else:
        return display_login_form(request, ERROR_MESSAGE)


def logout(request):
    request.session.flush()
    return HttpResponseRedirect('../index')

def display_login_form(request, error_message='', extra_context=None):
    request.session.set_test_cookie()
    context = {
               'title': 'Log in',
               'app_path': request.get_full_path(),
               'error_message': error_message,
               'is_login_page':True
               }
    context.update(extra_context or {})
    context_instance = RequestContext(request, current_app='students_app')
    return render_to_response('login.html', context,
                              context_instance=context_instance)


@is_authenticated
def view_groups(request):
    groups = Grup.objects.all().annotate(students_amount=Count('student'))
    return render_to_response('groups.html', {'groups':groups},
                              context_instance=RequestContext(request))


@is_authenticated
def view_students(request, group_name):
    students = Student.objects.all()
    return render_to_response('students.html', {'students':students},
                              context_instance=RequestContext(request))

@is_authenticated
def edit_group(request):
    """modifies or deletes Grup instance"""
    if request.method == 'POST' and request.POST:
        logging.debug(request.POST)
        if request.POST.get('oper') and request.POST['oper'] == 'del':
            try:
                Grup.objects.get(id=request.POST['id']).delete()
            except Exception, ex:
                logging.debug(ex)
        elif request.POST.get('oper') and request.POST['oper'] == 'add':
            instance = Grup()
            instance.name = request.POST.get('name')
            instance.student = Student.objects.get(id=request.POST.get('student'))
            try:
                instance.save()
            except Exception, ex:
                logging.debug(ex)
        else:
            try:
                instance = Grup.objects.get(id=request.POST.get('id'))
                instance.name = request.POST.get('name')
                instance.student = Student.objects.get(id=request.POST.get('student'))
                instance.save()
            except Exception, ex:
                logging.debug(ex)
        return render_to_response('grid-groups.html',
                                  context_instance=RequestContext(request))
    return HttpResponseNotFound('invalid request')


@is_authenticated
def edit_student(request):
    """modifies or deletes Student instance"""
    if request.method == 'POST' and request.POST:
        logging.debug(request.POST)
        instance = None
        if request.POST.get('oper') and request.POST['oper'] == 'del':
            try:
                Student.objects.get(id=request.POST['id']).delete()
            except Exception, ex:
                logging.debug(ex)
        elif request.POST.get('oper') and request.POST['oper'] == 'add':
            instance = Student()
        else:
            try:
                instance = Student.objects.get(id=request.POST.get('id'))
            except Exception, ex:
                logging.debug(ex)
        try:
            instance.surname = request.POST.get('surname')
            instance.name = request.POST.get('name')
            instance.patronymic = request.POST.get('patronymic')
            instance.birth_date = request.POST.get('birth_date')
            instance.student_card = request.POST.get('student_card')
            instance.grup = Grup.objects.get(id=request.POST.get('grup'))
            instance.save()
        except Exception, ex:
            logging.debug(ex)

        return render_to_response('grid-students.html',
                                  context_instance=RequestContext(request))
    return HttpResponseNotFound('invalid request')


def grid_handler(request, grid_name):
    """ handles pagination, sorting and searching"""
    logging.debug('grid handler %s' % grid_name)
    grid = class_for_name(grid_name, 'students_app.grids')()
    return HttpResponse(grid.get_json(request), mimetype="application/json")

def grid_config(request, grid_name):
    """build a config suitable to pass to jqgrid constructor"""
    logging.debug('grid config %s' % grid_name)
    grid = class_for_name(grid_name, 'students_app.grids')()
    return HttpResponse(grid.get_config(), mimetype="application/json")
