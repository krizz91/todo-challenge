from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Log(models.Model):
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)
    action = models.CharField(verbose_name=_('action'), max_length=10)
    related_id = models.IntegerField(verbose_name=_('related id'))

    class Meta:
        verbose_name = _('Log')
        verbose_name_plural = _('Logs')

    def __str__(self):
        return str(self.related_id) + " - " + self.action
