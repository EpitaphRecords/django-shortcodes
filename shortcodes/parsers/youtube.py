import re
from urllib import urlencode

from django import forms
from django.conf import settings
from django.template.loader import render_to_string

DEFAULT_WIDTH = 480
DEFAULT_HEIGHT = 270

def choicify(choice_tuple):
    return tuple((val, val,) for val in choice_tuple)

TRUTHY_CHOICES = choicify(('0', '1',))

class YoutubeParamForm(forms.Form):
    """
    These are shorthand/convenience parameters, `v` and `id` being synonymous (for a single video id)
    and `playlist_id`, `username`, `query` being shorthand for a playlist embed, YouTube user channel
    embed, and a search result embed, respectively
    """
    v = forms.CharField(required=False)
    id = forms.CharField(required=False)
    playlist_id = forms.CharField(required=False)
    username = forms.CharField(required=False)
    query = forms.CharField(required=False)

    # Embed size

    width = forms.CharField(required=False)
    height = forms.CharField(required=False)

    """
    YouTube embed parameters as taken from the documentation:
    https://developers.google.com/youtube/player_parameters#Parameters
    """

    autoplay = forms.ChoiceField(choices=TRUTHY_CHOICES, required=False)
    color = forms.ChoiceField(choices=choicify(('red', 'white',)), required=False)
    controls = forms.ChoiceField(choices=choicify(('0', '1', '2',)), required=False)
    cc_load_policy = forms.ChoiceField(choices=choicify(('1',)), required=False)
    disablekb = forms.ChoiceField(choices=TRUTHY_CHOICES, required=False)
    end = forms.IntegerField(min_value=1, required=False)
    fs = forms.ChoiceField(choices=TRUTHY_CHOICES, required=False)
    hl = forms.RegexField(regex=r'^[a-z]{2}$', required=False)
    iv_load_policy = forms.ChoiceField(choices=choicify(('1', '3',)), required=False)
    listType = forms.ChoiceField(choices=choicify(('playlist', 'search', 'user_uploads',)), required=False)
    loop = forms.ChoiceField(choices=TRUTHY_CHOICES, required=False)
    modestbranding = forms.ChoiceField(choices=choicify(('1',)), required=False)
    playlist = forms.CharField(required=False)
    playsinline = forms.ChoiceField(choices=TRUTHY_CHOICES, required=False)
    rel = forms.ChoiceField(choices=TRUTHY_CHOICES, required=False)
    showinfo = forms.ChoiceField(choices=TRUTHY_CHOICES, required=False)
    start = forms.IntegerField(min_value=1, required=False)

    def clean_width(self):
        width = self.cleaned_data.get('width')
        if not width:
            return getattr(settings, 'SHORTCODES_YOUTUBE_WIDTH', DEFAULT_WIDTH)
        return width

    def clean_height(self):
        height = self.cleaned_data.get('height')
        if not height:
            return getattr(settings, 'SHORTCODES_YOUTUBE_HEIGHT', DEFAULT_HEIGHT)
        return height

    def clean(self):
        data = super(YoutubeParamForm, self).clean()

        video_id = data.get('v') or data.get('id')
        playlist_id = data.get('playlist_id')
        username = data.get('username')
        query = data.get('query')

        if any([video_id, playlist_id, username, query]):
            if video_id:
                data['video_id'] = video_id
            elif playlist_id:
                data['list'] = playlist_id
                data['listType'] = 'playlist'
            elif username:
                data['list'] = username
                data['listType'] = 'user_uploads'
            elif query:
                data['list'] = query
                data['listType'] = 'search'

            return data
        else:
            raise forms.ValidationError('Must set a video id, playlist id or username for YouTube shortcode')

def parse(kwargs, template_name='shortcodes/youtube.html'):
    form = YoutubeParamForm(kwargs)

    if form.is_valid():

        # Pull out cleaned data, filtering out empty values
        
        data = dict((k, v) for k, v in form.cleaned_data.iteritems() if v)

        # Pop these out, leaving the remaining keys for the query string

        for key in ['playlist_id', 'username', 'query']:
            data.pop(key, None)

        ctx = {
            'video_id': data.pop('video_id', None),
            'width': data.pop('width'),
            'height': data.pop('height')
        }

        ctx['query_string'] = urlencode(data)

        return render_to_string(template_name, ctx)
