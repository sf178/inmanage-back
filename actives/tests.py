from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Property, Transport, Business, ActivesIncome, ActivesExpenses
from front.models import CustomUser
from balance.models import Balance, Card


class UserAssetsTests(APITestCase):

    def setUp(self):
        # Создание тестового пользователя
        self.user_data = {
            'phone_number': '+79871620432',
            'password': 'testpassword',
            # Добавьте другие необходимые поля
        }
        self.user = CustomUser.objects.create_user(**self.user_data)
        response = self.client.post(reverse('login'), {'phone_number': '+79871620432', 'password': 'testpassword'})
        response_json = response.json()
        self.token = response_json.get('access')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_create_and_update_assets(self):
        # Создание недвижимости
        property_data = {
            'name': 'Test Property',
            'address': '123 Test Street',
            'owner': 'Owner 1',
            'rent_type': True,
            'bought_price': 100000.00,
            'actual_price': 110000.00,
            'revenue': 10000.00,
            'equipment_price': 5000.00,
            'average_profit': 1000.00,
            'loan': False,
            'month_income': 5000.00,
            'month_expense': 2000.00,
            # Дополнительные поля
        }
        property_response = self.client.post(reverse('property-list-create'), property_data)
        self.assertEqual(property_response.status_code, status.HTTP_201_CREATED)
        property_id = property_response.data['id']

        # Создание транспорта
        transport_data = {
            'mark': 'Test Mark',
            'model': 'Test Model',
            'owner': 'Owner 2',
            'owner_type': True,
            'vin': '1234567890ABCDEFG',
            'use': 'Personal',
            'bought_price': 50000.00,
            'average_market_price': 55000.00,
            'min_market_price': 45000.00,
            'max_market_price': 60000.00,
            'loan': False,
            'month_income': 2000.00,
            'month_expense': 500.00,
            # Дополнительные поля
        }
        transport_response = self.client.post(reverse('transport-list-create'), transport_data)
        self.assertEqual(transport_response.status_code, status.HTTP_201_CREATED)
        transport_id = transport_response.data['id']

        # Создание бизнеса
        business_data = {
            'name': 'Test Business',
            'address': '456 Business Ave',
            'type': 'Retail',
            'direction': 'Local',
            'bought_price': 200000.00,
            'month_income': 15000.00,
            'month_expense': 5000.00,
            'own_funds': True,
            'own_funds_amount': 50000.00,
            # Дополнительные поля
        }
        business_response = self.client.post(reverse('business-list-create'), business_data)
        self.assertEqual(business_response.status_code, status.HTTP_201_CREATED)
        business_id = business_response.data['id']

        # Создание доходов и расходов для недвижимости
        property_income_data = {
            'property': property_id,
            'funds': 3000.00,
            'comment': 'Rent income'
        }
        property_expenses_data = {
            'property': property_id,
            'funds': 1000.00,
            'category': 'Maintenance',
            'title': 'Repair work',
            'description': 'Fixing the roof'
        }
        self.client.post(reverse('income-list'), property_income_data)
        self.client.post(reverse('expenses-list'), property_expenses_data)

        # Создание доходов и расходов для транспорта
        transport_income_data = {
            'transport': transport_id,
            'funds': 2000.00,
            'comment': 'Transport service income'
        }
        transport_expenses_data = {
            'transport': transport_id,
            'funds': 500.00,
            'category': 'Fuel',
            'title': 'Gas expenses',
            'description': 'Monthly gas cost'
        }
        self.client.post(reverse('income-list'), transport_income_data)
        self.client.post(reverse('expenses-list'), transport_expenses_data)

        # Создание доходов и расходов для бизнеса
        business_income_data = {
            'business': business_id,
            'funds': 10000.00,
            'comment': 'Monthly sales'
        }
        business_expenses_data = {
            'business': business_id,
            'funds': 3000.00,
            'category': 'Salary',
            'title': 'Employee wages',
            'description': 'Monthly salary payment'
        }
        self.client.post(reverse('income-list'), business_income_data)
        self.client.post(reverse('expenses-list'), business_expenses_data)

        # Проверка изменения баланса
        balance_response = self.client.get(reverse('balance-list'))
        self.assertEqual(balance_response.status_code, status.HTTP_200_OK)
        self.assertGreater(balance_response.data['total_income'], 0)
        self.assertGreater(balance_response.data['total_expenses'], 0)

        # Проверка, что доходы и расходы корректно добавлены в активы
        property_updated = Property.objects.get(id=property_id)
        self.assertGreater(property_updated.total_income, 0)
        self.assertGreater(property_updated.total_expense, 0)

        transport_updated = Transport.objects.get(id=transport_id)
        self.assertGreater(transport_updated.total_income, 0)
        self.assertGreater(transport_updated.total_expense, 0)

        business_updated = Business.objects.get(id=business_id)
        self.assertGreater(business_updated.total_income, 0)
        self.assertGreater(business_updated.total_expense, 0)

if __name__ == '__main__':
    import unittest
    unittest.main()
