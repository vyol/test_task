from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.tag(name="edit_list")
def do_edit_list(parser, token):
    try:
        tag_name, obj_name, app_label = token.contents.split()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly 2 arguments"
                                           % token.contents.split()[0])
    return EditListNode(obj_name, app_label)

class EditListNode(template.Node):
    def __init__(self, obj_name, app_label):
        self.obj = template.Variable(obj_name)
        self.app_label = template.Variable(app_label)

    def render(self, context):
        class_name = type(self.obj.resolve(context)).__name__
        url = r"/admin/%s/%s" % (self.app_label, class_name.lower())
        inner_text = "edit %s list" % class_name
        try:
            return mark_safe(u'<a href="%s">%s</a>' % (url, inner_text))
        except template.VariableDoesNotExist:
            return ''


