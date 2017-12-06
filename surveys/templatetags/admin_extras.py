import json

from django import template
from django.contrib.postgres.forms import JSONField

register = template.Library()


@register.filter
def is_json_field(field):
    return isinstance(field.field.field, JSONField)


@register.filter
def load_json(value):
    return json.loads(value)
