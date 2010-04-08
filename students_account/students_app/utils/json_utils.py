import datetime
import logging
from decimal import Decimal
from django.core.serializers.json import DateTimeAwareJSONEncoder
from django.db.models import Model
from django.db.models.query import QuerySet
from django.utils import simplejson as json
from django.utils.functional import Promise
from django.utils.encoding import force_unicode, smart_str
from django.utils.html import escape
from students_app.utils.main_utils import class_for_name, table_to_class_name


#try:
#    # we need it, if we want to serialize query- and model-objects
#    # of google appengine within json_encode
#    from google import appengine
#except:
appengine = None


def json_encode_obj(data):
    """
    The main issues with django's default json serializer is that properties that
    had been added to an object dynamically are being ignored (and it also has 
    problems with some models).
    """

    def _any(data):
        ret = None
        # Opps, we used to check if it is of type list, but that fails 
        # i.e. in the case of django.newforms.utils.ErrorList, which extends
        # the type "list". Oh man, that was a dumb mistake!
        if isinstance(data, list):
            ret = _list(data)
        # Same as for lists above.
        elif appengine and isinstance(data, appengine.ext.db.Query):
            ret = _list(data)
        elif isinstance(data, dict):
            ret = _dict(data)
        elif isinstance(data, Decimal):
            # json.dumps() cant handle Decimal
            ret = str(data)
        elif isinstance(data, QuerySet):
            # Actually its the same as a list ...
            ret = _list(data)
        elif isinstance(data, Model):
            ret = _model(data)
        elif appengine and isinstance(data, appengine.ext.db.Model):
            ret = _googleModel(data)
        # here we need to encode the string as unicode (otherwise we get utf-16 in the json-response)
        elif isinstance(data, basestring):
            ret = escape(unicode(data))
        # see http://code.djangoproject.com/ticket/5868
        elif isinstance(data, Promise):
            ret = force_unicode(data)
        elif isinstance(data, datetime.datetime):
            # For dojo.date.stamp we convert the dates to use 'T' as separator instead of space
            # i.e. 2008-01-01T10:10:10 instead of 2008-01-01 10:10:10
            ret = str(data)#.replace(' ', 'T')
        elif isinstance(data, datetime.date):
            ret = str(data)
        elif isinstance(data, datetime.time):
            #ret = "T" + str(data)
            ret = str(data)
        else:
            ret = data
        return ret

    def _model(data):
        ret = {}
        # If we only have a model, we only want to encode the fields.

        #for f in data._meta.fields:
        #    if hasattr(f, 'related'):
        #        kls = class_for_name(table_to_class_name(getattr(f, 'name')))
        #        str_val = kls.objects.get(id=getattr(data, f.attname))
        #        ret[f.attname] = unicode(str_val)
        #    else:
        #        ret[f.attname] = _any(getattr(data, f.attname))


        for f in data._meta.fields:
            if f.attname.endswith('_id'):
                attname = f.attname[:-3]
                ret[attname] = force_unicode(class_for_name(table_to_class_name(attname)).\
                                        objects.get(id=_any(getattr(data, f.attname))))
                print ret[attname]
            else:
                ret[f.attname] = _any(getattr(data, f.attname))
        #for f in data._meta.fields:
        #    ret[f.attname] = _any(getattr(data, f.attname))
        # And additionally encode arbitrary properties that had been added.
        fields = dir(data.__class__) + ret.keys()
        add_ons = [k for k in dir(data) if k not in fields]
        for k in add_ons:
            ret[k] = _any(getattr(data, k))
        return ret

    def _googleModel(data):
        ret = {}
        ret['id'] = data.key().id()
        for f in data.fields():
            ret[f] = _any(getattr(data, f))
        return ret

    def _list(data):
        ret = []
        for v in data:
            ret.append(_any(v))
        return ret

    def _dict(data):
        import operator
        ret = {}
        #for k, v in data.items():
        #    ret[k] = _any(v)

        #foreign_key_repr
        for k, v in data.items():
            try:
                kls = class_for_name(table_to_class_name(k))
                str_val = kls.objects.get(id=v)
                ret[k] = unicode(str_val)
            except AttributeError:
                ret[k] = _any(v)
            except Exception, ex:
                logging.debug(ex)
        return ret

    ret = _any(data)
    return ret

def json_encode(data):
    ret = json_encode_obj(data)
    return json.dumps(ret, cls=DateTimeAwareJSONEncoder)

def json_decode(json_string):
    """
    This function is just for convenience/completeness (because we have json_encode).
    Sometimes you want to convert a json-string to a python object.
    It throws a ValueError, if the JSON String is invalid.
    """
    return json.loads(json_string)
