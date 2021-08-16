from django import template
import time
register = template.Library()

@register.simple_tag
def tiempo(tiempo):
    return str(int(tiempo/3600)) + ":" + time.strftime('%M:%S', time.gmtime(tiempo))