from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *
from .serializers import *


@receiver(post_save, sender=TodoItem)
def update_todo_task(sender, instance, **kwargs):
    if not instance.done and instance.task.done:
        instance.task.done = False
        instance.task.save()


@receiver(post_save, sender=TodoTask)
def update_project(sender, instance, **kwargs):
    if not instance.done and instance.project.done:
        instance.project.done = False
        instance.project.save()