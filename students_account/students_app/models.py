from django.contrib.auth.models import User, UserManager
from django.db import models
from django.db.models.signals import post_save, post_delete

class MyLog(models.Model):
    model_name = models.CharField(max_length=32)
    inst = models.CharField(max_length=32)
    time = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=8)

    def __unicode__(self):
        return u'%s %s - %s %s' % (self.model_name, self.inst,
                                       self.time, self.action)

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


def log_save(instance, created, **kwargs):
    act = created and 'create' or 'save'
    log_entry = MyLog(model_name=type(instance).__name__,
                    inst=unicode(instance)[:31], action=act)
    log_entry.save()

def log_delete(instance, **kwargs):
    log_entry = MyLog(model_name=type(instance).__name__,
                    inst=unicode(instance)[:31], action='delete')
    log_entry.save()

post_save.connect(log_save, sender=Grup, dispatch_uid="log_save_grup_uid")
post_save.connect(log_save, sender=Student, dispatch_uid="log_save_stud_uid")
post_delete.connect(log_delete, sender=Grup, dispatch_uid="log_del_grup_uid")
post_delete.connect(log_delete, sender=Student, dispatch_uid="log_del_stud_uid")
