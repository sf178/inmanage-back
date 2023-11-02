from django.db import models


class ExpensePersonalCategory(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, null=True, blank=True)
    is_default = models.BooleanField(default=False, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.name


class ExpenseGeneralCategory(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, null=True, blank=True)
    is_default = models.BooleanField(default=False, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.name


class ExpenseSubCategory(models.Model):
    id = models.AutoField(primary_key=True)
    general_category = models.ForeignKey(ExpenseGeneralCategory, related_name="subcategories", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name