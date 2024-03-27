from django.contrib.contenttypes.models import ContentType
from django.db import models

from inventory.models import Inventory
from passives.models import Loans
from simple_history.models import HistoricalRecords
from datetime import datetime, timezone

from test_backend.custom_methods import PathAndRename


# Create your models here.


class MillisecondDateTimeField(models.DateTimeField):

    def pre_save(self, model_instance, add):
        """
        Возвращает поле для сохранения в базе данных.
        Если поле имеет auto_now или auto_now_add установленное в True,
        это будет также обновлено.
        """
        if self.auto_now or (self.auto_now_add and add):
            current_time = datetime.now(timezone.utc)
            formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            value = datetime.strptime(formatted_time, '%Y-%m-%dT%H:%M:%S.%f%z')
            setattr(model_instance, self.attname, value)
            return value
        return super(MillisecondDateTimeField, self).pre_save(model_instance, add)


class Jewelry(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    name = models.TextField(blank=True, null=True)
    purchase_cost = models.FloatField(blank=True, null=True, default=0.0)
    estimated_cost = models.FloatField(blank=True, null=True, default=0.0)
    comment = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='jewelry_photos/', blank=True, null=True)
    income = models.ManyToManyField('actives.ActivesIncome', blank=True, related_name='+')
    expenses = models.ManyToManyField('actives.ActivesExpenses', blank=True, related_name='+')
    total_income = models.FloatField(blank=True, null=True, default=0.0)
    total_expense = models.FloatField(blank=True, null=True, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name or ''


class Securities(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    name = models.TextField(blank=True, null=True)
    broker = models.TextField(blank=True, null=True)
    cost = models.FloatField(blank=True, null=True, default=0.0)
    market_price = models.FloatField(blank=True, null=True, default=0.0)
    income = models.ManyToManyField('actives.ActivesIncome', blank=True, related_name='+')
    expenses = models.ManyToManyField('actives.ActivesExpenses', blank=True, related_name='+')
    total_income = models.FloatField(blank=True, null=True, default=0.0)
    total_expense = models.FloatField(blank=True, null=True, default=0.0)
    count = models.IntegerField(blank=True, null=True)
    sum = models.FloatField(blank=True, null=True, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name or ''


class Property(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    name = models.TextField(blank=True)
    square = models.FloatField(blank=True, null=True, default=0.0)
    city = models.TextField(blank=True, null=True)
    street = models.TextField(blank=True, null=True)
    building_number = models.TextField(blank=True, null=True)
    owner = models.TextField(blank=True, null=True)
    rent_type = models.TextField(blank=True, null=True)
    rent_price = models.FloatField(blank=True, null=True, default=0.0)
    bought_price = models.FloatField(blank=True, null=True, default=0.0)
    actual_price = models.FloatField(blank=True, null=True, default=0.0)
    revenue = models.FloatField(blank=True, null=True, default=0.0)
    equipment_price = models.FloatField(blank=True, null=True, default=0.0)
    equipment = models.ForeignKey('inventory.Inventory', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    average_profit = models.FloatField(blank=True, null=True, default=0.0)

    #### loans part ####
    loan = models.BooleanField(blank=True, null=True) # loan indicator
    loan_link = models.ForeignKey(Loans, on_delete=models.SET_NULL, related_name='property_loan_link', null=True,
                                  blank=True)
    initial_payment = models.FloatField(blank=True, null=True, default=0.0)
    loan_term = models.BigIntegerField(blank=True, null=True)
    percentage = models.FloatField(blank=True, null=True, default=0.0)
    month_payment = models.FloatField(blank=True, null=True, default=0.0)
    #### loans part

    month_income = models.FloatField(blank=True, null=True, default=0.0)
    month_expense = models.FloatField(blank=True, null=True, default=0.0)
    income = models.ManyToManyField('actives.ActivesIncome', blank=True, related_name='+')
    expenses = models.ManyToManyField('actives.ActivesExpenses', blank=True, related_name='+')
    total_income = models.FloatField(blank=True, null=True, default=0.0)
    total_expense = models.FloatField(blank=True, null=True, default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return f'Property {self.name} of user with ID {self.user_id}'

    class Meta:
        verbose_name = 'property'
        verbose_name_plural = 'property'
        ordering = ('id',)


class Transport(models.Model):
    id = models.AutoField(primary_key=True)
    #brand = models.TextField(blank=True)
    mark = models.TextField(blank=True, null=True)
    #name = models.TextField(blank=True, null=True)
    model = models.TextField(blank=True, null=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    owner_count = models.TextField(blank=True, null=True)
    owner_type = models.BooleanField(blank=True, null=True)
    # vin = models.CharField(max_length=17, blank=True, null=True)
    year = models.TextField(blank=True, null=True)
    use = models.TextField(blank=True, null=True)
    bought_price = models.FloatField(blank=True, null=True, default=0.0)
    average_market_price = models.FloatField(blank=True, null=True, default=0.0)
    min_market_price = models.FloatField(blank=True, null=True, default=0.0)
    max_market_price = models.FloatField(blank=True, null=True, default=0.0)
    images = models.ManyToManyField('actives.TransportImage', blank=True, related_name='+')


    #### loans part ####
    loan = models.BooleanField(blank=True, null=True)  # loan indicator
    loan_link = models.ForeignKey('passives.Loans', on_delete=models.SET_NULL, blank=True, null=True, related_name='+')

    initial_payment = models.FloatField(blank=True, null=True, default=0.0)
    loan_term = models.FloatField(blank=True, null=True, default=0.0)
    percentage = models.FloatField(blank=True, null=True, default=0.0)
    month_payment = models.FloatField(blank=True, null=True, default=0.0)
    #### loans part

    month_income = models.FloatField(blank=True, null=True, default=0.0)
    month_expense = models.FloatField(blank=True, null=True, default=0.0)
    income = models.ManyToManyField('actives.ActivesIncome', blank=True, related_name='+')
    expenses = models.ManyToManyField('actives.ActivesExpenses', blank=True, related_name='+')
    total_income = models.FloatField(blank=True, null=True, default=0.0)
    total_expense = models.FloatField(blank=True, null=True, default=0.0)
    average_profit = models.FloatField(blank=True, null=True, default=0.0)
    revenue = models.FloatField(blank=True, null=True, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()
    def __str__(self):
        return f'ID: {self.id}'

    def create(self, validated_data):
        images_data = validated_data.pop('images', None)
        transport = Transport.objects.create(**validated_data)
        if images_data:
            for image_data in images_data:
                TransportImage.objects.create(transport=transport, **image_data)
        return transport

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', None)
        # Обновите поля instance здесь
        if images_data:
            instance.images.all().delete()  # Перед добавлением новых изображений удаляем старые
            for image_data in images_data:
                TransportImage.objects.create(transport=instance, **image_data)
        return super().update(instance, validated_data)

    class Meta:
        verbose_name = 'transport'
        verbose_name_plural = 'transport'
        ordering = ('id',)


class TransportImage(models.Model):
    id = models.AutoField(primary_key=True)
    transport = models.ForeignKey('actives.Transport', on_delete=models.CASCADE, blank=True, related_name='+')
    image = models.ImageField(upload_to=PathAndRename('actives_transport_images/'), blank=True, null=True)
    def __str__(self):
        return f'ID: {self.id}'

    class Meta:
        verbose_name = 'transport-image'
        verbose_name_plural = 'transport-image'
        ordering = ('id',)


class Business(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    direction = models.TextField(blank=True, null=True)
    bought_price = models.FloatField(blank=True, null=True, default=0.0)
    card = models.ForeignKey('balance.Card', on_delete=models.DO_NOTHING, blank=True, null=True)
    #investment_type = models.TextField()
    total_worth = models.FloatField(blank=True, null=True, default=0.0)
    month_income = models.FloatField(blank=True, null=True, default=0.0)
    month_expense = models.FloatField(blank=True, null=True, default=0.0)
    income = models.ManyToManyField('actives.ActivesIncome', blank=True, related_name='+')
    expenses = models.ManyToManyField('actives.ActivesExpenses', blank=True, related_name='+')
    total_income = models.FloatField(blank=True, null=True, default=0.0)
    total_expense = models.FloatField(blank=True, null=True, default=0.0)
    average_profit = models.FloatField(blank=True, null=True, default=0.0)
    revenue = models.FloatField(blank=True, null=True, default=0.0)
    own_funds = models.BooleanField(blank=True, null=True, default=True)  # loan indicator
    own_funds_amount = models.FloatField(blank=True, null=True, default=0.0)
    equipment = models.ForeignKey('inventory.Inventory', on_delete=models.CASCADE, blank=True, null=True)
    third_party_tools = models.FloatField(blank=True, null=True, default=0.0)
    third_party_tools_percentage = models.FloatField(blank=True, null=True, default=0.0)
    creditor = models.TextField(blank=True, null=True)
    #### loans part ####
    loan = models.BooleanField(blank=True, null=True)  # loan indicator
    loan_link = models.ForeignKey('passives.Loans', on_delete=models.SET_NULL, blank=True, null=True, related_name='+')

    initial_payment = models.FloatField(blank=True, null=True, default=0.0)
    loan_term = models.FloatField(blank=True, null=True, default=0.0)
    percentage = models.FloatField(blank=True, null=True, default=0.0)
    month_payment = models.FloatField(blank=True, null=True, default=0.0)

    #### loans part
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return f'ID: {self.id}'



    class Meta:
        verbose_name = 'business'
        verbose_name_plural = 'businesses'
        ordering = ('id',)



# # # # # # # это перенести в приложение по ценным бумагам (securities, to be made...)
#
# class Stocks(models.Model):
#     id = models.AutoField(primary_key=True)
#     SHORTNAME = models.TextField(blank=True)
#     OPEN = models.FloatField(blank=True, null=True, default=0.0)
#     LOW = models.FloatField(blank=True, null=True, default=0.0)
#     HIGH = models.FloatField(blank=True, null=True, default=0.0)
#
#     def __str__(self):
#         return f'ID: {self.id}'
#
#     class Meta:
#         verbose_name = 'stock'
#         verbose_name_plural = 'stocks'
#         ordering = ('id',)
#
#
# class Bonds(models.Model):
#     id = models.AutoField(primary_key=True)
#     SHORTNAME = models.TextField()
#     OPEN = models.FloatField(blank=True, null=True, default=0.0)
#     LOW = models.FloatField(blank=True, null=True, default=0.0)
#     HIGH = models.FloatField(blank=True, null=True, default=0.0)
#     MARKETPRICE2 = models.FloatField(blank=True, null=True, default=0.0)
#     MARKETPRICE3 = models.FloatField(blank=True, null=True, default=0.0)
#
#
#     def __str__(self):
#         return f'ID: {self.id}'
#
#     class Meta:
#         verbose_name = 'bond'
#         verbose_name_plural = 'bonds'
#         ordering = ('id',)
#
#
# class Securities(models.Model):
#     id = models.AutoField(primary_key=True)
#     user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
#
#     def __str__(self):
#         return f'ID: {self.id}'
#
#     class Meta:
#         verbose_name = 'securities'
#         verbose_name_plural = 'securities'
#         ordering = ('id',)
#
# # # # # # # # # # # # # # # # #



class ActivesIncome(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    property = models.ForeignKey('actives.Property', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    transport = models.ForeignKey('actives.Transport', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    business = models.ForeignKey('actives.Business', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    writeoff_account = models.ForeignKey('balance.Card', on_delete=models.CASCADE, blank=True, null=True)
    child = models.ForeignKey('balance.Income', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    funds = models.FloatField(blank=True, null=True, default=0.0)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ActivesExpenses(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    property = models.ForeignKey('actives.Property', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    transport = models.ForeignKey('actives.Transport', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    business = models.ForeignKey('actives.Business', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    # category = models.ForeignKey('category.ActivesCategory', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    child = models.ForeignKey('balance.Expenses', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    writeoff_account = models.ForeignKey('balance.Card', on_delete=models.CASCADE, blank=True, null=True)
    funds = models.FloatField(blank=True, null=True, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)


class MainProperties(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, related_name='+')
    total_funds = models.FloatField(blank=True, null=True, default=0.0)
    total_income = models.FloatField(blank=True, null=True, default=0.0)
    total_expenses = models.FloatField(blank=True, null=True, default=0.0)
    properties = models.ManyToManyField(Property, blank=True, null=True)
    def __str__(self):
        return f'ID: {self.id}'


class MainTransport(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, related_name='+')
    total_funds = models.FloatField(blank=True, null=True, default=0.0)
    total_income = models.FloatField(blank=True, null=True, default=0.0)
    total_expenses = models.FloatField(blank=True, null=True, default=0.0)
    transport = models.ManyToManyField(Transport, blank=True, null=True)
    def __str__(self):
        return f'ID: {self.id}'


class MainBusinesses(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, related_name='+')
    total_funds = models.FloatField(blank=True, null=True, default=0.0)
    total_income = models.FloatField(blank=True, null=True, default=0.0)
    total_expenses = models.FloatField(blank=True, null=True, default=0.0)
    businesses = models.ManyToManyField(Business, blank=True, null=True)


class MainJewelry(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, related_name='+')
    total_funds = models.FloatField(blank=True, null=True, default=0.0)
    total_income = models.FloatField(blank=True, null=True, default=0.0)
    total_expenses = models.FloatField(blank=True, null=True, default=0.0)
    jewelries = models.ManyToManyField(Jewelry, blank=True, null=True)


class MainSecurities(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, related_name='+')
    total_funds = models.FloatField(blank=True, null=True, default=0.0)
    total_income = models.FloatField(blank=True, null=True, default=0.0)
    total_expenses = models.FloatField(blank=True, null=True, default=0.0)
    securities = models.ManyToManyField(Securities, blank=True, null=True)


class MainDeposits(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, related_name='+')
    total_funds = models.FloatField(blank=True, null=True, default=0.0)
    total_income = models.FloatField(blank=True, null=True, default=0.0)
    total_expenses = models.FloatField(blank=True, null=True, default=0.0)
    deposits = models.ManyToManyField('actives_deposit.ActivesDeposit', blank=True, null=True)


# class MainLoans(models.Model):
#     id = models.AutoField(primary_key=True)
#     user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, related_name='+')
#     total_funds = models.FloatField(blank=True, null=True, default=0.0)
#     loans = models.ManyToManyField('actives_deposit.ActivesLoans', blank=True, null=True)


class Actives(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE)
    properties = models.ForeignKey(MainProperties, on_delete=models.DO_NOTHING, blank=True, related_name='+', null=True)
    transports = models.ForeignKey(MainTransport, on_delete=models.DO_NOTHING, blank=True, related_name='+', null=True)
    businesses = models.ForeignKey(MainBusinesses, on_delete=models.DO_NOTHING, blank=True, related_name='+', null=True)
    jewelries = models.ForeignKey(MainJewelry, on_delete=models.DO_NOTHING, blank=True, related_name='+', null=True)
    securities = models.ForeignKey(MainSecurities, on_delete=models.DO_NOTHING, blank=True, related_name='+', null=True)
    deposits = models.ForeignKey(MainDeposits, on_delete=models.DO_NOTHING, blank=True, related_name='+', null=True)
    # loans = models.ForeignKey(MainLoans, on_delete=models.DO_NOTHING, blank=True, related_name='+', null=True)
    total_funds = models.FloatField(blank=True, null=True, default=0.0)
    total_income = models.FloatField(blank=True, null=True, default=0.0)
    total_expenses = models.FloatField(blank=True, null=True, default=0.0)

    def __str__(self):
        return f'ID: {self.id}'

    class Meta:
        verbose_name = 'actives'
        verbose_name_plural = 'actives'
        ordering = ('id',)


class ObjectsProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE)
    actives = models.ManyToManyField(Actives, blank=True)
    passives = models.ManyToManyField('passives.Passives', blank=True)

    def __str__(self):
        return f'Profile: ID - {self.id}; user - {self.user_id}'

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'
        ordering = ('id',)

