from django.db import models

class Category(models.Model):
    # Общие поля для всех категорий
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    icon_id = models.IntegerField()

    def __str__(self):
        return self.title

class PersonalExpenseCategory(Category):
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, null=True, blank=True)

class AssetCategory(Category):
    ASSET_CHOICES = [
        ('real_estate', 'Недвижимость'),
        ('transport', 'Транспорт'),
        ('business', 'Бизнес'),
    ]
    asset_type = models.CharField(max_length=255, choices=ASSET_CHOICES)

class LiabilityCategory(Category):
    LIABILITY_CHOICES = [
        ('real_estate', 'Недвижимость'),
        ('loans', 'Кредиты'),
        ('transport', 'Транспорт'),
    ]
    liability_type = models.CharField(max_length=255, choices=LIABILITY_CHOICES)


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