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
    bought_price = models.FloatField(blank=True, null=True)
    actual_price = models.FloatField(blank=True, null=True)
    
    #### loans part ####
    loan = models.BooleanField(blank=True, null=True) # loan indicator
    initial_payment = models.FloatField(blank=True, null=True)
    loan_term = models.FloatField(blank=True, null=True)
    percentage = models.FloatField(blank=True, null=True)
    month_payment = models.FloatField(blank=True, null=True)
    #### loans part

    revenue = models.FloatField(blank=True, null=True)
    equipment_price = models.FloatField(blank=True, null=True)
    month_income = models.FloatField(blank=True, null=True)
    month_expense = models.FloatField(blank=True, null=True)
    total_income = models.FloatField(blank=True, null=True)
    total_expense = models.FloatField(blank=True, null=True)
    average_profit = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return f'Property {self.name} of user with ID {self.user_id}'

    class Meta:
        verbose_name = 'property'
        verbose_name_plural = 'property'
        ordering = ('id',)


class PropertyAsset(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    price = models.FloatField()
    done = models.BooleanField(null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return f'Asset {self.name} of property with ID {self.property}'

    class Meta:
        verbose_name = 'property_asset'
        verbose_name_plural = 'property_asset'
        ordering = ('id',)


class Transport(models.Model):
    id = models.AutoField(primary_key=True)
    #brand = models.TextField(blank=True)
    mark = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    model = models.TextField(blank=True, null=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    owner = models.TextField(blank=True, null=True)
    owner_type = models.BooleanField(blank=True, null=True)
    vin = models.CharField(max_length=17, blank=True, null=True)
    use = models.TextField(blank=True, null=True)
    bought_price = models.FloatField(blank=True, null=True)
    average_market_price = models.FloatField(blank=True, null=True)
    min_market_price = models.FloatField(blank=True, null=True)
    max_market_price = models.FloatField(blank=True, null=True)
    images = models.ManyToManyField('actives.TransportImage', blank=True, null=True, related_name='+')


    #### loans part ####
    loan = models.BooleanField(blank=True, null=True)  # loan indicator
    initial_payment = models.FloatField(blank=True, null=True)
    loan_term = models.FloatField(blank=True, null=True)
    percentage = models.FloatField(blank=True, null=True)
    month_payment = models.FloatField(blank=True, null=True)
    #### loans part

    month_income = models.FloatField(blank=True, null=True)
    month_expense = models.FloatField(blank=True, null=True)
    total_income = models.FloatField(blank=True, null=True)
    total_expense = models.FloatField(blank=True, null=True)
    average_profit = models.FloatField(blank=True, null=True)
    revenue = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    #
    # def create_loan_object(self):
    #     if self.loan:
    #         loan = Loans(
    #             user_id=self.user_id,
    #             name=self.name,
    #             remainder=self.bought_price - self.initial_payment,
    #             sum=self.bought_price,
    #             loan_term=self.loan_term,
    #             percentage=self.percentage,
    #             month_payment=self.month_payment,
    #             maintenance_cost=self.month_expense
    #         )
    #         loan.save()

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
    #investment_type = models.TextField()
    month_income = models.FloatField(blank=True, null=True)
    month_expense = models.FloatField(blank=True, null=True)
    total_income = models.FloatField(blank=True, null=True)
    total_expense = models.FloatField(blank=True, null=True)
    average_profit = models.FloatField(blank=True, null=True)
    revenue = models.FloatField(blank=True, null=True)
    own_funds = models.FloatField(blank=True, null=True)
    third_party_tools = models.FloatField(blank=True, null=True)
    third_party_tools_percentage = models.FloatField(blank=True, null=True)
    creditor = models.TextField(blank=True)
    #### loans part ####
    loan = models.BooleanField(blank=True, null=True)  # loan indicator
    initial_payment = models.FloatField(blank=True, null=True)
    loan_term = models.FloatField(blank=True, null=True)
    percentage = models.FloatField(blank=True, null=True)
    month_payment = models.FloatField(blank=True, null=True)

    #### loans part
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    #
    # def create_loan_object(self):
    #     if self.loan:
    #         loan = Loans(
    #             user_id=self.user_id,
    #             name=self.name,
    #
    #             loan_term=self.loan_term,
    #             percentage=self.percentage,
    #             month_payment=self.month_payment,
    #             maintenance_cost=self.month_expense
    #         )
    #         loan.save()

    def __str__(self):
        return f'ID: {self.id}'

    class Meta:
        verbose_name = 'business'
        verbose_name_plural = 'businesses'
        ordering = ('id',)


class BusinessAsset(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    price = models.FloatField(blank=True, null=True)
    done = models.BooleanField(null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return f'Asset {self.name} of business with ID {self.business_id}'

    class Meta:
        verbose_name = 'business_asset'
        verbose_name_plural = 'business_asset'
        ordering = ('id',)


class Stocks(models.Model):
    id = models.AutoField(primary_key=True)
    SHORTNAME = models.TextField(blank=True)
    OPEN = models.FloatField(blank=True, null=True)
    LOW = models.FloatField(blank=True, null=True)
    HIGH = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f'ID: {self.id}'

    class Meta:
        verbose_name = 'stock'
        verbose_name_plural = 'stocks'
        ordering = ('id',)


class Bonds(models.Model):
    id = models.AutoField(primary_key=True)
    SHORTNAME = models.TextField()
    OPEN = models.FloatField(blank=True, null=True)
    LOW = models.FloatField(blank=True, null=True)
    HIGH = models.FloatField(blank=True, null=True)
    MARKETPRICE2 = models.FloatField(blank=True, null=True)
    MARKETPRICE3 = models.FloatField(blank=True, null=True)

        #models.FloatField()

    def __str__(self):
        return f'ID: {self.id}'

    class Meta:
        verbose_name = 'bond'
        verbose_name_plural = 'bonds'
        ordering = ('id',)


class Income(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey('actives.Property', on_delete=models.CASCADE, blank=True, null=True)
    transport = models.ForeignKey('actives.Transport', on_delete=models.CASCADE, blank=True, null=True)
    business = models.ForeignKey('actives.Business', on_delete=models.CASCADE, blank=True, null=True)
    funds = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Expenses(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey('actives.Property', on_delete=models.CASCADE, blank=True, null=True)
    transport = models.ForeignKey('actives.Transport', on_delete=models.CASCADE, blank=True, null=True)
    business = models.ForeignKey('actives.Business', on_delete=models.CASCADE, blank=True, null=True)
    funds = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Actives(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE)
    properties = models.ManyToManyField(Property, blank=True)
    transports = models.ManyToManyField(Transport, blank=True)
    businesses = models.ManyToManyField(Business, blank=True)
    stocks = models.ManyToManyField(Stocks, blank=True)
    bonds = models.ManyToManyField(Bonds, blank=True)
    total_income = models.FloatField(blank=True, null=True)
    total_expenses = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f'ID: {self.id}'

    class Meta:
        verbose_name = 'actives_scripts'
        verbose_name_plural = 'actives_scripts'
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

