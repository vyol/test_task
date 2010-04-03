from django.db import models

# Create your models here.
class Grup(models.Model):
    name = models.CharField(max_length=16, unique=True)
    captain = models.ForeignKey('Student', related_name='captain',
                                null=True, blank=True)

    def __unicode__(self):
        return u'%s %s' % (self.name, self.captain)


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

