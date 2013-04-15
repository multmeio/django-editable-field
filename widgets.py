#!/usr/bin/env python
# encoding: utf-8

from django.utils.safestring import mark_safe
from django.forms.widgets import Input
from django.core.exceptions import ImproperlyConfigured


class XEditableWidget(Input):
    input_type = 'hidden'

    class Media:
        css = {
            'all': ('foobar.css',)
        }
        js = ('foo.js', 'bar.js')

    def __init__(self, *args, **kwargs):
        if not 'model' in kwargs or not 'data_source' in kwargs:
            raise ImproperlyConfigured(
                "You must define a 'model' or a 'data_source' to the XEditableWidget"
            )
        self.title = kwargs.pop('title', "Click here to Edit")
        self.model = kwargs.pop('model', None)
        self.data_source = kwargs.pop('data_source', None)
        super(XEditableWidget, self).__init__(*args, **kwargs)

    def get_xeditable_template(self, name, value):
        return """<a href="javascript:;" class="tip-right x_editable_field"
           data-hidden="#id_%(field_id)s"
           data-type="typeahead" data-source="%(field_url)s"
           data-original-title="%(title)s">
              %(field_value)s
        </a>""" % {
            'field_id': self.id_for_label(name),
            'field_url': self.data_source,
            'field_value': self.model.objects.get(pk=value),
            'title': self.title,
        }

    def render(self, name, value, attrs=None):
        return mark_safe(u'%s%s' % (
            self.get_xeditable_template(name, value),
            super(XEditableWidget, self).render(name, value, attrs)
        ))
