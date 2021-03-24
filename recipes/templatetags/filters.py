from django import template
from django.contrib.auth import get_user_model


User = get_user_model()
register = template.Library()

TENSES = {
    1: '',
    2: 'а',
    3: 'а',
    4: 'а',
}


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def tense(text, count):
    end = int(count) % 100
    end = end if end in (11, 12, 13, 14) else end % 10
    end = TENSES.get(end, "ов")
    return f'{text}{end}'
