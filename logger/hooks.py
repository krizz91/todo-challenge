from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from todo.models import Tasks
from logger.models import Log

@receiver(post_save, sender=Tasks, dispatch_uid="task_creation")
def task_creation(sender, instance=None, created=False, **kwargs):
    if created:
        new_log = Log()
        new_log.action = "CREATION"
        new_log.related_id = instance.id
        new_log.save()

@receiver(pre_save, sender=Tasks, dispatch_uid="task_complete")
def task_complete(sender, instance=None, **kwargs):
    if (instance.id is not None):
        old = Tasks.objects.get(id=instance.id)
        if old.completed != instance.completed:
            new_log = Log()
            new_log.action = "COMPLETED"
            new_log.related_id = instance.id
            new_log.save()
