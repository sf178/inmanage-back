from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver

from balance.models import Card
from .models import *
from .serializers import *
from django.db import transaction
from balance.models import Card as Card, Income as BalIncome, Expenses as BalExpenses


@receiver(post_save, sender=Income)
def create_income_from_planner(sender, instance, created, **kwargs):
    if created:
        content_object = None
        card = Card.objects.get(id=instance.writeoff_account.id, user=instance.user)
        if instance.task:
            content_object = instance.task
        elif instance.item:
            content_object = instance.item
        elif instance.project:
            content_object = instance.project

        if content_object:
            content_type = ContentType.objects.get_for_model(content_object)
            income_instance = BalIncome.objects.create(
                user=instance.user,
                writeoff_account=instance.writeoff_account,
                funds=instance.funds,
                comment=instance.comment,
                content_type=content_type,
                object_id=content_object.id
            )
            card.income.add(income_instance)
            instance.child = income_instance
            instance.save(update_fields=['child'])
        update_project_totals(instance, is_income=True)


@receiver(post_save, sender=Expenses)
def create_expenses_from_planner(sender, instance, created, **kwargs):
    if created:
        card = Card.objects.get(id=instance.writeoff_account.id, user=instance.user)
        content_object = None
        if instance.task:
            content_object = instance.task
        elif instance.item:
            content_object = instance.item
        elif instance.project:
            content_object = instance.project

        if content_object:
            content_type = ContentType.objects.get_for_model(content_object)
            expenses_instance = BalExpenses.objects.create(
                user=instance.user,
                writeoff_account=instance.writeoff_account,
                title=instance.title,
                description=instance.description,
                funds=instance.funds,
                content_type=content_type,
                object_id=content_object.id
            )
            card.expenses.add(expenses_instance)
            instance.child = expenses_instance
            instance.save(update_fields=['child'])
        update_project_totals(instance, is_income=False)


def update_project_totals(instance, is_income):
    project = get_project_from_instance(instance)

    if project:
        update_totals_for_project(project)


def get_project_from_instance(instance):
    # Получение проекта из экземпляра дохода или расхода
    if instance.task:
        return instance.task.project
    elif instance.item:
        return instance.item.task.project
    elif instance.project:
        return instance.project
    return None


def update_totals_for_project(project):
    # Обновление общего дохода и расхода для проекта
    project.total_income = calculate_total(project, is_income=True)
    project.total_expenses = calculate_total(project, is_income=False)
    project.save()


def calculate_total(project, is_income):
    total = 0
    if is_income:
        related_field = 'income'
    else:
        related_field = 'expenses'

    # Доходы/расходы проекта
    for entry in getattr(project, related_field).all():
        total += entry.funds

    # Доходы/расходы связанных задач и подзадач
    for task in project.tasks_list.all():
        for entry in getattr(task, related_field).all():
            total += entry.funds

        for item in task.desc_list.all():
            for entry in getattr(item, related_field).all():
                total += entry.funds

    return total


@receiver(post_save, sender=TodoItem)
def update_todo_task(sender, instance, **kwargs):
    if getattr(instance, '_is_put_request', False):
        return

    if not instance.done and instance.task.done:
        instance.task.done = False
        instance.task.save()


@receiver(post_save, sender=TodoTask)
def update_project(sender, instance, **kwargs):
    if getattr(instance, '_is_put_request', False):
        return

    # Проверка на наличие атрибута 'project' в экземпляре
    if instance.project and not instance.done and instance.project.done:
        instance.project.done = False
        instance.project.save()

