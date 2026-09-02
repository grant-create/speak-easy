from django import template

register = template.Library()


@register.filter
def duration(seconds):
    if seconds is None:
        return '—'
    seconds = int(seconds)
    minutes, secs = divmod(seconds, 60)
    if minutes:
        return f'{minutes}m {secs}s'
    return f'{secs}s'
