from django.contrib import admin
from students_app.models import Grup, MyLog, Student

#class StudentInline(admin.TabularInline):
#    model = Student
#    extra = 1

#class GrupAdmin(admin.ModelAdmin):
#    inlines = [StudentInline]

#admin.site.register(Grup, GrupAdmin)
admin.site.register(Grup)
admin.site.register(Student)
admin.site.register(MyLog)

