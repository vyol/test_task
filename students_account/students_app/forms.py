from django import forms
from django.forms import widgets
from students_app.models import Grup, Student

class StudentForm(forms.ModelForm):
    pk = forms.IntegerField(widget=widgets.HiddenInput,
                            required=False)
    class Meta:
        model = Student

class GroupForm(forms.ModelForm):
    pk = forms.IntegerField(widget=widgets.HiddenInput,
                            required=False)
    class Meta:
        model = Grup
