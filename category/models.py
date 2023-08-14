from django.db import models



class ExpensePersonalSubcategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey('category.ExpensePersonalCategory', related_name='subcategories', on_delete=models.CASCADE)

class ExpensePersonalCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    sub_categories = models.ManyToManyField(ExpensePersonalSubcategory, blank=True, related_name='+')
