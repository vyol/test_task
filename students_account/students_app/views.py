# Create your views here.
from django.contrib import auth
from django.forms.util import ValidationError
from django.http import HttpResponseRedirect
from django.db.models import Count
from django.shortcuts import render_to_response
from django.template import RequestContext
from students_app.models import Grup, Student
from students_app.forms import GroupForm, StudentForm
from students_app.utils.main_utils import is_authenticated

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


def display_login_form(request, error_message='', extra_context=None):
    request.session.set_test_cookie()
    context = {
               'title': 'Log in',
               'app_path': request.get_full_path(),
               'error_message': error_message
               }
    context.update(extra_context or {})
    context_instance = RequestContext(request, current_app='students_app')
    return render_to_response('login.html', context,
                              context_instance=context_instance)


@is_authenticated
def view_groups(request):
    groups = Grup.objects.all().annotate(students_amount=Count('student'))
    if request.method == 'POST' and request.POST:
        form = GroupForm(request.POST)
        if form.is_valid():
            try:
                form.validate_unique()
                form.save()
            except (ValidationError, ValueError):
                inst = Grup.objects.get(pk=request.POST['pk'])
                form = GroupForm(request.POST, instance=inst)
                form.save()
            except Exception, e:
                print e
            form = GroupForm()
        return render_to_response('groups.html',
                              {'groups':groups, 'form':form})
    form = GroupForm()
    return render_to_response('groups.html',
                              {'groups':groups, 'form':form})


@is_authenticated
def view_students(request, group_name):
    students = Student.objects.filter(grup__name=group_name)
    if request.method == 'POST' and request.POST:
        form = StudentForm(request.POST)
        if form.is_valid():
            try:
                form.validate_unique()
                form.save()
            except ValidationError, e:
                inst = Student.objects.get(pk=request.POST['pk'])
                form = StudentForm(request.POST, instance=inst)
                form.save()
            except Exception, e:
                print e
            form = StudentForm()
        return render_to_response('students.html',
                              {'students':students, 'form':form})
    form = StudentForm()
    return render_to_response('students.html',
                              {'students':students, 'form':form})


@is_authenticated
def delete_student(request, student_pk):
    student = Student.objects.get(pk=student_pk)
    group_name = student.grup.name
    Student.objects.get(pk=student_pk).delete()
    return HttpResponseRedirect('../%s' % group_name)


@is_authenticated
def delete_group(request, group_pk):
    Grup.objects.get(pk=group_pk).delete()
    return HttpResponseRedirect('../')
