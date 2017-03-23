import re

from django.template.loader import render_to_string
from django.conf import settings

DEFAULT_WIDTH = 480
DEFAULT_HEIGHT = 166

HEX_COLOR_REGEX = r'^([a-f0-9]{6}|[a-f0-9]{3})$'

def parse(kwargs, template_name='shortcodes/soundcloud.html'):
    """
    Shortcode parser for Soundcloud player embed
    https://soundcloud.com/pages/embed
    """
    url = kwargs.get('url')

    if url:
        width = kwargs.get(
            'width',
            getattr(settings, 'SHORTCODES_SOUNDCLOUD_WIDTH', DEFAULT_WIDTH)
        )

        height = kwargs.get(
            'height',
            getattr(settings, 'SHORTCODES_SOUNDCLOUD_HEIGHT', DEFAULT_HEIGHT)
        )

        color = kwargs.get('color')

        if color and not re.match(HEX_COLOR_REGEX, color, flags=re.IGNORECASE):
            color = None

        ctx = {
            'url': url,
            'width': width,
            'height': height
        }

        if color:
            ctx['color'] = color

        return render_to_string(template_name, ctx)
