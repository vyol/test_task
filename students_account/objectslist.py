from django.core.management.base import AppCommand
from optparse import make_option

class Command(AppCommand):
    option_list = AppCommand.option_list + (
        make_option('--model', action='append', dest='model',
            help='Add object count information'),
    )
    help = 'Prints object list for given application and model (optional).'
    args = '[appname --model ModelName]'
    requires_model_validation = True

    def handle_app(self, app, **options):
        from django.db.models import get_models
        lines = []
        if options['model']:
            model = [m for m in get_models(app) if m.__name__ == options['model'][0]][0]
            return '[%s]' % options['model'][0] + '\n\t' \
                    + '\n\t'.join([str(o) for o in model.objects.all()])
        for model in get_models(app):
            obj = model.objects.all()
            lines.append("[%s]" % model.__name__ + '\n\t'
                         + '\n\t'.join([str(o) for o in obj]))
        return "\n".join(lines)
