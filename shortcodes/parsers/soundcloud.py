import re

from django.conf import settings

from .base import BaseParser

DEFAULT_WIDTH = 480
DEFAULT_HEIGHT = 166
DEFAULT_CSS_CLASS = 'shortcode-soundcloud'

HEX_COLOR_REGEX = r'^([a-f0-9]{6}|[a-f0-9]{3})$'

class SoundcloudParser(BaseParser):
    name = 'soundcloud'

    def get_context(self, context={}, render_format='html'):
        """
        Shortcode parser for Soundcloud player embed
        https://soundcloud.com/pages/embed
        """
        ctx = {}
        url = context.get('url')

        if url:
            width = context.get(
                'width',
                getattr(settings, 'SHORTCODES_SOUNDCLOUD_WIDTH', DEFAULT_WIDTH)
            )

            height = context.get(
                'height',
                getattr(settings, 'SHORTCODES_SOUNDCLOUD_HEIGHT', DEFAULT_HEIGHT)
            )

            color = context.get('color')

            if color and not re.match(HEX_COLOR_REGEX, color, flags=re.IGNORECASE):
                color = None

            ctx = {
                'css_class': getattr(settings, 'SHORTCODES_SOUNDCLOUD_CSS_CLASS', DEFAULT_CSS_CLASS),
                'url': url,
                'width': width,
                'height': height
            }

            if color:
                ctx['color'] = color

        context.update(ctx)
        return context
