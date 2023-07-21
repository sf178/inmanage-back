# from django.test import TestCase
# from django.urls import reverse
# from rest_framework.test import APIClient, APITestCase
# from rest_framework import status
# from .models import *
# from .serializers import *
# from front.models import CustomUser
#
#
# class PropertyTests(APITestCase):
#     def setUp(self):
#         self.user_id = 1
#         self.property1 = Property.objects.create(
#             user_id=self.user_id,
#             name='Test Property 1',
#             address='123 Test St',
#             owner='Test Owner 1',
#             actual_price=100000,
#             bought_price=90000,
#             initial_payment=20000,
#             loan_term=30,
#             percentage=4,
#             month_payment=500,
#             revenue=1500,
#             rent_type=1,
#             equipment_price=5000,
#             month_income=2000,
#             month_expense=500,
#             average_profit=1000
#         )
#         self.property2 = Property.objects.create(
#             user_id=self.user_id,
#             name='Test Property 2',
#             address='456 Test St',
#             owner='Test Owner 2',
#             actual_price=200000,
#             bought_price=180000,
#             initial_payment=40000,
#             loan_term=30,
#             percentage=4,
#             month_payment=800,
#             revenue=2000,
#             rent_type=0,
#             equipment_price=10000,
#             month_income=3000,
#             month_expense=1000,
#             average_profit=2000
#         )
#
#     def test_create_property(self):
#         url = reverse('property-list-create')
#         data = {
#             'user_id': self.user_id,
#             'name': 'New Property',
#             'address': '789 Test St',
#             'owner': 'Test Owner 3',
#             'actual_price': 300000,
#             'bought_price': 270000,
#             'initial_payment': 60000,
#             'loan_term': 30,
#             'percentage': 4,
#             'month_payment': 1200,
#             'revenue': 4000,
#             'rent_type': 1,
#             'equipment_price': 20000,
#             'month_income': 5000,
#             'month_expense': 2000,
#             'average_profit': 3000
#         }
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Property.objects.count(), 3)
#         prop = Property.objects.get(name='New Property')
#         serializer = PropertySerializer(prop)
#         self.assertEqual(response.data, serializer.data)
#
#     def test_list_properties(self):
#         url = reverse('property-list-get')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         properties = Property.objects.all()
#         serializer = PropertySerializer(properties, many=True)
#         self.assertEqual(response.data, serializer.data)
#
#     def test_filter_properties_by_user_id(self):
#         url = reverse('property-list-get')
#         response = self.client.get(url, {'user_id': self.user_id})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         properties = Property.objects.filter(user_id=self.user_id)
#         serializer = PropertySerializer(properties, many=True)
#         self.assertEqual(response.data, serializer.data)
#
#     def test_delete_property(self):
#         url = reverse('property-list-delete', args=[self.property1.id])
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(Property.objects.count(), 1)
#         self.assertFalse(Property.objects.filter(id=self.property1.id).exists())
#
#     def test_update_property(self):
#         url = reverse('property-list-update', args=[self.property2.id])
#         data = {
#             'user_id': self.user_id,
#             'name': 'New Property',
#             'address': '789 Test St',
#             'owner': 'Test Owner 3',
#             'actual_price': 300000,
#             'bought_price': 270000,
#             'initial_payment': 60000,
#             'loan_term': 30,
#             'percentage': 4,
#             'month_payment': 1200,
#             'revenue': 4000,
#             'rent_type': 1,
#             'equipment_price': 20000,
#             'month_income': 5000,
#             'month_expense': 2000,
#             'average_profit': 3000
#         }
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Property.objects.count(), 3)
#         prop = Property.objects.get(name='New Property')
#         serializer = PropertySerializer(prop)
#         self.assertEqual(response.data, serializer.data)