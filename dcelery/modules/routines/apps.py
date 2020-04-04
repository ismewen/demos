"""Django Application configuration."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

__all__ = ['BeatConfig']


class BeatConfig(AppConfig):
    """Default configuration for routines app."""

    name = 'common.apps.routines'
    label = 'routines'
    verbose_name = _('Periodic Tasks')
