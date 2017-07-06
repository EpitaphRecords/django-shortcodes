from django.conf import settings

from .base import BaseParser

DEFAULT_CSS_CLASS = 'shortcode-vimeo'

class VimeoParser(BaseParser):
    name = 'vimeo'

    def get_context(self, context={}, render_format='html'):
        ctx = {}
        video_id = context.get('id')

        if video_id:
            width = getattr(settings, 'SHORTCODES_VIMEO_WIDTH', 480)
            height = getattr(settings, 'SHORTCODES_VIMEO_HEIGHT', 385)

            ctx = {
                'css_class': getattr(settings, 'SHORTCODES_VIMEO_CSS_CLASS', DEFAULT_CSS_CLASS),
                'video_id': video_id,
                'width': width,
                'height': height
            }
        
        context.update(ctx)
        return context
