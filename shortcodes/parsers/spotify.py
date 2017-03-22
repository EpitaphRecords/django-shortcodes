from django.template.loader import render_to_string
from django.conf import settings

THEME_OPTIONS = ('black', 'white',)
VIEW_OPTIONS = ('list', 'coverart',)

DEFAULT_WIDTH = 480
DEFAULT_HEIGHT = 480

def parse(kwargs, template_name='shortcodes/spotify.html'):
    """
    Shortcode parser for Spotify player embed. All options and markup referenced from:
    https://developer.spotify.com/technologies/widgets/spotify-play-button/
    """
    uri = kwargs.get('uri')

    if uri:
        width = kwargs.get(
            'width',
            getattr(settings, 'SHORTCODES_SPOTIFY_WIDTH', DEFAULT_WIDTH)
        )

        height = kwargs.get(
            'height',
            getattr(settings, 'SHORTCODES_SPOTIFY_HEIGHT', DEFAULT_HEIGHT)
        )

        theme = kwargs.get('theme')
        view = kwargs.get('view')

        ctx = {
            'uri': uri,
            'width': width,
            'height': height
        }

        if theme and theme in THEME_OPTIONS:
            ctx['theme'] = theme

        if view and view in VIEW_OPTIONS:
            ctx['view'] = view

        return render_to_string(template_name, ctx)

