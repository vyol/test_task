import logging
from django.db.models import Count
from django.utils.html import escape
from django.utils.encoding import smart_str
from students_app.jqgrid import JqGrid
from students_app.models import Grup, Student

def _get_values(kls, key_attr, repr_attr=''):
    res = {}
    for obj in kls.objects.all():
        res[smart_str(escape(getattr(obj, key_attr)))] = \
            unicode(getattr(obj, repr_attr, None) or obj)
    return res

class GrupGrid(JqGrid):

    queryset = Grup.objects.all().annotate(students_amount=Count('grup'))
    print queryset
    fields = ['id', 'name', 'student', 'students_amount']
    url = '/jqgrid/GrupGrid/'#reverse('grid_handler')#
    editurl = '/edit/group/'#reverse('grid_handler')#
    caption = 'Groups'

    colmodel_overrides = {
        'id' : {'index': 'id', 'width': 30, 'align': 'left', 'editable': False,
                'searchoptions' : {'sopt' :
                                   ['eq', 'ne', 'lt', 'le', 'ge', 'gt', 'in']}},
        'name' : {'searchoptions' : {'sopt' : ['eq', 'ne']},
                  'formatter':'link'},
        'student' : {'label':u'Captain', 'stype' : 'select',
                      'searchoptions' :{'sopt' : ['eq', 'ne']},
                      'edittype':"select",
                      'editoptions':{'value':_get_values(Student, 'id')}},
        'students_amount' : {'searchoptions' :{'sopt' :
                                    ['eq', 'ne', 'lt', 'le', 'ge', 'gt', 'in']}}
    }

    def get_default_config(self,):
        config = JqGrid.get_default_config(self)
        config_overrides = {'sortname':('id'), 'sortorder':'desc'}
        config.update(config_overrides)
        return config

    def lookup_foreign_key_field(self, options, field_name):
        try:
            return super(GrupGrid, self).lookup_foreign_key_field(options, field_name)
        except Exception, e:
            logging.debug(e)
            return (field_name, None, True, False)

    def field_to_colmodel(self, field, field_name):
        colmodel = {
            'name': field_name,
            'index': field_name,
            'label': field_name,
            'editable': True
        }
        return colmodel


class StudentGrid(JqGrid):

    #model = Student
    queryset = Student.objects.all()
    fields = ['id', 'surname', 'name', 'patronymic', 'birth_date', 'grup', 'student_card']
    url = '/jqgrid/StudentGrid/'
    editurl = '/edit/student/'
    caption = 'Students'

    colmodel_overrides = {
         'id' : {'index': 'id', 'width': 30, 'align': 'left',
                 'editable': False, 'searchoptions' :{'sopt' :
                                ['eq', 'ne', 'lt', 'le', 'ge', 'gt', 'in']}},
        'grup' : {'label':u'Grup', 'width' : 100, 'stype' : 'select',
                      'searchoptions' : {'sopt' : ['eq', 'ne']},
                      'edittype':"select",
                      'editoptions':{'value':_get_values(Grup, 'id'), 'size':"20"}},
    }

    def get_default_config(self):
        config = JqGrid.get_default_config(self)
        config_overrides = {'sortname':('id'), 'sortorder':'desc'}
        config.update(config_overrides)
        return config
