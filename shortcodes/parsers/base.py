from django.conf import settings
from django.template.loader import render_to_string

SHORTCODES_FORMATS = ('html', 'amp',)

SHORTCODES_SETTING_PREFIX = 'SHORTCODES_'

SHORTCODES_TEMPLATE_DIR = 'shortcodes'


class BaseParser(object):
    name = None

    def get_setting(self, name):
        return '%s%s' % (SHORTCODES_SETTING_PREFIX, name.upper())

    def get_template_name(self, render_format):
        return '%s/%s.%s' % (SHORTCODES_TEMPLATE_DIR, self.name, render_format)

    def get_context(self, context={}, render_format='html'):
        return context

    def render(self, context, render_format='html'):
        if render_format not in SHORTCODES_FORMATS:
            raise ValueError('Invalid render format specified')
        
        ctx = self.get_context(context, render_format)
        template_name = self.get_template_name(render_format)
        return render_to_string(template_name, ctx)
