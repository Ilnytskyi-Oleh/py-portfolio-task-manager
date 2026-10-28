from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs) -> str:
    """Build query string from current GET, overriding given keys."""
    request = context["request"]
    query = request.GET.copy()
    for key, value in kwargs.items():
        if value is None or value == "":
            query.pop(key, None)
        else:
            query[key] = value
    encoded = query.urlencode()
    return f"?{encoded}" if encoded else "?"


@register.simple_tag(takes_context=True)
def sort_link(context, field: str) -> str:
    """Toggle sort direction for a column."""
    request = context["request"]
    current = request.GET.get("sort", "deadline")
    direction = request.GET.get("dir", "asc")
    if current == field and direction == "asc":
        new_dir = "desc"
    else:
        new_dir = "asc"
    return url_replace(context, sort=field, dir=new_dir, page=None)
