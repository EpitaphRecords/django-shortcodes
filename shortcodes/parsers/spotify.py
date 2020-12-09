from django.conf import settings

from .base import BaseParser

THEME_OPTIONS = ('black', 'white',)
VIEW_OPTIONS = ('list', 'coverart',)

DEFAULT_WIDTH = 480
DEFAULT_HEIGHT = 480
DEFAULT_CSS_CLASS = 'shortcode-spotify'

class SpotifyParser(BaseParser):
    name = 'spotify'

    def get_context(self, context={}, render_format='html'):
        """
        Shortcode parser for Spotify player embed. All options and markup referenced from:
        https://developer.spotify.com/technologies/widgets/spotify-play-button/
        """
        ctx = {}
        uri = context.get('uri')

        if uri:
            width = context.get(
                'width',
                getattr(settings, 'SHORTCODES_SPOTIFY_WIDTH', DEFAULT_WIDTH)
            )

            height = context.get(
                'height',
                getattr(settings, 'SHORTCODES_SPOTIFY_HEIGHT', DEFAULT_HEIGHT)
            )

            theme = context.get('theme')
            view = context.get('view')

            ctx = {
                'css_class': getattr(settings, 'SHORTCODES_SPOTIFY_CSS_CLASS', DEFAULT_CSS_CLASS),
                'uri': uri,
                'width': width,
                'height': height
            }

            if theme and theme in THEME_OPTIONS:
                ctx['theme'] = theme

            if view and view in VIEW_OPTIONS:
                ctx['view'] = view

        context.update(ctx)
        return context

