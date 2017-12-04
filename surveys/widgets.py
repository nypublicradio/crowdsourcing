from django.forms import Widget
from django.utils.html import format_html


class AudioPlaybackWidget(Widget):
    def render(self, name, value, attrs=None, renderer=None):
        return format_html('<audio name="{}" src="{}" controls />', name, value)
