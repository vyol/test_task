from django.db import models

# Create your models here.
class Grup(models.Model):
    name = models.CharField(max_length=16, unique=True)

    def __unicode__(self):
        return self.name + u''


class Student(models.Model):
    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    patronymic = models.CharField(max_length=32)
    birth_date = models.DateField()
    student_card = models.CharField(max_length=16)
    grup = models.ForeignKey(Grup)

    def __unicode__(self):
        return u'%s %s' % (self.surname, self.name)

    class Meta:
        unique_together = [('surname', 'name', 'patronymic')]


class Captain(models.Model):
    grup = models.ForeignKey(Grup)
    student = models.ForeignKey(Student)

    def __unicode__(self):
        return u'%s %s' % (self.grup, self.student)
