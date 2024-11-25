from django import template

register = template.Library()


@register.filter(name="lower_initials")
def lowercase_initials(value):
    """Returns initials of space-separated string in lowercase."""
    return "".join(word[0] for word in value.lower().split()[:2:])
