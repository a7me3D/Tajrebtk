from django import template

register = template.Library()

@register.filter(name="index")
def _index(query, n):
    try:
        return query[n]
    except:
        return None