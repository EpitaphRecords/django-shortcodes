from shortcodes import parser
from django import template


register = template.Library()


SHORTCODE_FORMATS = ('html', 'amp',)

@register.filter(name='shortcodes', is_safe=True)
def shortcodes_replace(value, render_format='html'):
    if render_format not in SHORTCODE_FORMATS:
        raise template.TemplateSyntaxError('Invalid format specified for shortcodes')
    return parser.parse(value, render_format=render_format)



