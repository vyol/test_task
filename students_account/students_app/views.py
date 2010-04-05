# Create your views here.
from django.http import HttpResponseRedirect
from django.db.models import Count
from django.shortcuts import render_to_response
from students_app.models import Grup, Student
from students_app.forms import GroupForm, StudentForm

def view_groups(request):
    groups = Grup.objects.all().annotate(students_amount=Count('student'))
    if request.method == 'POST' and request.POST:
        form = GroupForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                inst = Grup.objects.get(pk=cd['pk'])
            except Grup.DoesNotExist:
                inst = Grup()
            inst.name = cd['name']
            inst.student_card = cd['captain']
            try:
                inst.save()
            except Exception, e:
                print e
        return render_to_response('students.html',
                              {'students':students, 'form':form})
    form = GroupForm()
    return render_to_response('groups.html',
                              {'groups':groups, 'form':form})

def view_students(request, group_name):
    students = Student.objects.filter(grup__name=group_name)
    if request.method == 'POST' and request.POST:
        form = StudentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                inst = Student.objects.get(pk=cd['pk'])
            except Student.DoesNotExist:
                inst = Student()
            inst.surname = cd['surname']
            inst.name = cd['name']
            inst.patronymic = cd['patronymic']
            inst.birth_date = cd['birth_date']
            inst.student_card = cd['student_card']
            inst.grup = cd['grup']
            try:
                inst.save()
            except Exception, e:
                print e
        return render_to_response('students.html',
                              {'students':students, 'form':form})                
    form = StudentForm()
    return render_to_response('students.html',
                              {'students':students, 'form':form})

def delete_student(request, student_pk):
    student = Student.objects.get(pk=student_pk)
    group_name = student.grup.name
    Student.objects.get(pk=student_pk).delete()
    return HttpResponseRedirect('../%s' % group_name)

def delete_group(request, group_pk):
    Grup.objects.get(pk=group_pk).delete()
    return HttpResponseRedirect('../')
