from django.db import models


class ExpensePersonalSubcategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey('category.ExpensePersonalCategory', related_name='subcategories', on_delete=models.CASCADE)


class ExpensePersonalCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    sub_categories = models.ManyToManyField(ExpensePersonalSubcategory, blank=True, related_name='+')


class ExpenseGeneralCategory(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    subcategories = models.ManyToManyField('category.ExpenseGeneralSubCategory', blank=True, related_name='+')  # Добавляем связь с подкатегориями
    def __str__(self):
        return self.name


class ExpenseGeneralSubCategory(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    nested_subcategories = models.ManyToManyField('category.ExpenseGeneralNestedSubCategory', blank=True)  # Добавляем связь с подвложенными категориями
    general_category = models.ForeignKey('category.ExpenseGeneralCategory', related_name="+", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.general_category} -> {self.name}"


class ExpenseGeneralNestedSubCategory(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    sub_category = models.ForeignKey('category.ExpenseGeneralSubCategory', related_name="+", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.sub_category.general_category} -> {self.sub_category} -> {self.name}"