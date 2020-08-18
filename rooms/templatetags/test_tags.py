from django import template

register = template.Library()


@register.filter
def test_tags(value):
    print(value)
    return "testFilter"
