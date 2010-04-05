from django.contrib.auth.models import User, UserManager
from django.db import models

# Create your models here.
class Grup(models.Model):
    name = models.CharField(max_length=16, unique=True)
    captain = models.ForeignKey('Student', related_name='captain',
                                null=True, blank=True)

    def __unicode__(self):
        return self.name + u''


class Student(models.Model):
    surname = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    patronymic = models.CharField(max_length=32)
    birth_date = models.DateField()
    student_card = models.CharField(max_length=16)
    grup = models.ForeignKey(Grup)

    def __unicode__(self):
        return u'%s %s' % (self.surname, self.name)

    class Meta:
        unique_together = [('surname', 'name', 'patronymic')]
