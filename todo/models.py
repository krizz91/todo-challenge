from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Tasks(models.Model):
    """
    This model store a list of tasks

    Attributes:
    created (DateTime): This field store the task's creation datetime. It's readonly
    description (Text): This field adds a short description of the task
    completed (Boolean): This boolean field indicates if the task is completed or not
    """

    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(verbose_name=_('Description'))
    completed = models.BooleanField(verbose_name=_('Completed'), default=False)

    def complete(self):
        self.completed = True
        self.save()

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

    def __str__(self):
        return self.description