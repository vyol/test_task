# Create your views here.
from django.db.models import Count
from django.shortcuts import render_to_response
from students_app.models import Grup, Student

def view_groups(request):
    groups = Grup.objects.all().annotate(students_amount=Count('student'))
    return render_to_response('groups.html', {'groups':groups})

def view_students(request, group_name):
    students = Student.objects.filter(grup__name=group_name)
    return render_to_response('students.html', {'students':students})
