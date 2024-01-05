from django.db import models


class Category(models.Model):
    # Общие поля для всех категорий
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    icon_id = models.IntegerField(blank=True, null=True)
    subcategory = models.ForeignKey('category.SubCategory', related_name='+', on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.title


class SubCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class PersonalCategory(Category):
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, null=True, blank=True)





