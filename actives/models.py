from django.db import models
from passives.models import Loans
from simple_history.models import HistoricalRecords

# Create your models here.
class Property(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    name = models.TextField(blank=True)
    address = models.TextField(blank=True)
    owner = models.TextField(blank=True)
    rent_type = models.BooleanField(blank=True, null=True)
    bought_price = models.FloatField(blank=True, null=True, default=0.0)
    actual_price = models.FloatField(blank=True, null=True, default=0.0)
    revenue = models.FloatField(blank=True, null=True, default=0.0)
    equipment_price = models.FloatField(blank=True, null=True, default=0.0)
    equipment = models.ForeignKey('inventory.Inventory', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    average_profit = models.FloatField(blank=True, null=True, default=0.0)

    #### loans part ####
    loan = models.BooleanField(blank=True, null=True) # loan indicator
    loan_link = models.ForeignKey(Loans, on_delete=models.CASCADE, related_name='property_loan_link', null=True,
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
    owner = models.TextField(blank=True, null=True)
    owner_type = models.BooleanField(blank=True, null=True)
    vin = models.CharField(max_length=17, blank=True, null=True)
    use = models.TextField(blank=True, null=True)
    bought_price = models.FloatField(blank=True, null=True, default=0.0)
    average_market_price = models.FloatField(blank=True, null=True, default=0.0)
    min_market_price = models.FloatField(blank=True, null=True, default=0.0)
    max_market_price = models.FloatField(blank=True, null=True, default=0.0)
    images = models.ManyToManyField('actives.TransportImage', blank=True, related_name='+')


    #### loans part ####
    loan = models.BooleanField(blank=True, null=True)  # loan indicator
    loan_link = models.ForeignKey('passives.Loans', on_delete=models.DO_NOTHING, blank=True, null=True, related_name='+')

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

    class Meta:
        verbose_name = 'transport'
        verbose_name_plural = 'transport'
        ordering = ('id',)


class TransportImage(models.Model):
    id = models.AutoField(primary_key=True)
    transport = models.ForeignKey('actives.Transport', on_delete=models.CASCADE, blank=True, related_name='+')
    image = models.ImageField(upload_to='actives_transport_images/', blank=True, null=True)
    def __str__(self):
        return f'ID: {self.id}'

    class Meta:
        verbose_name = 'transport-image'
        verbose_name_plural = 'transport-image'
        ordering = ('id',)

class Business(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True)
    address = models.TextField(blank=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, blank=True, null=True)
    type = models.BooleanField(blank=True, null=True)
    direction = models.TextField(blank=True)
    bought_price = models.FloatField(blank=True, null=True, default=0.0)
    #investment_type = models.TextField()
    month_income = models.FloatField(blank=True, null=True, default=0.0)
    month_expense = models.FloatField(blank=True, null=True, default=0.0)
    income = models.ManyToManyField('actives.ActivesIncome', blank=True, related_name='+')
    expenses = models.ManyToManyField('actives.ActivesExpenses', blank=True, related_name='+')
    total_income = models.FloatField(blank=True, null=True, default=0.0)
    total_expense = models.FloatField(blank=True, null=True, default=0.0)
    average_profit = models.FloatField(blank=True, null=True, default=0.0)
    revenue = models.FloatField(blank=True, null=True, default=0.0)
    own_funds = models.FloatField(blank=True, null=True, default=0.0)
    equipment = models.ForeignKey('inventory.Inventory', on_delete=models.CASCADE, blank=True, null=True)
    third_party_tools = models.FloatField(blank=True, null=True, default=0.0)
    third_party_tools_percentage = models.FloatField(blank=True, null=True, default=0.0)
    creditor = models.TextField(blank=True)
    #### loans part ####
    loan = models.BooleanField(blank=True, null=True)  # loan indicator
    loan_link = models.ForeignKey('passives.Loans', on_delete=models.DO_NOTHING, blank=True, null=True, related_name='+')

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
    funds = models.FloatField(blank=True, null=True, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)


class ActivesExpenses(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    property = models.ForeignKey('actives.Property', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    transport = models.ForeignKey('actives.Transport', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    business = models.ForeignKey('actives.Business', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
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


class Actives(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE)
    properties = models.ForeignKey(MainProperties, on_delete=models.DO_NOTHING, blank=True, related_name='+', null=True)
    transports = models.ForeignKey(MainTransport, on_delete=models.DO_NOTHING, blank=True, related_name='+', null=True)
    businesses = models.ForeignKey(MainBusinesses, on_delete=models.DO_NOTHING, blank=True, related_name='+', null=True)
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

