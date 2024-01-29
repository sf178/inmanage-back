from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import *
from .serializers import *
from balance.models import Card, Income, Expenses
from todo.models import Project
from todo.models import Income as prj_income


@receiver(post_save, sender=WorkIncome)
def create_income_from_actives(sender, instance, created, **kwargs):
    if created:
        content_object = None
        card = Card.objects.get(id=instance.writeoff_account.id, user=instance.user)
        prj = Project.objects.get(id=instance.project.id, user=instance.user)

        if instance.work:
            content_object = instance.work
            content_type = ContentType.objects.get_for_model(content_object)
            income_instance = Income.objects.create(
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
        elif instance.project:
            content_object = instance.project
            income_instance = prj_income.objects.create(
                user=instance.user,
                writeoff_account=instance.writeoff_account,
                funds=instance.funds,
                comment=instance.comment,
                project=instance.project
            )
            prj.income.add(income_instance)
            instance.child = income_instance
            instance.save(update_fields=['child'])

        # if content_object:
        #     content_type = ContentType.objects.get_for_model(content_object)
        #     income_instance = Income.objects.create(
        #         user=instance.user,
        #         writeoff_account=instance.writeoff_account,
        #         funds=instance.funds,
        #         comment=instance.comment,
        #         content_type=content_type,
        #         object_id=content_object.id
        #     )
        #     card.income.add(income_instance)
        #     instance.child = income_instance
        #     instance.save(update_fields=['child'])