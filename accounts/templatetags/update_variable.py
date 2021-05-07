from django.template.defaulttags import register

@register.simple_tag
def update_variable(value):
    """Allows to update existing variable in template"""
    return value