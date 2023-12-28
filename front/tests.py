# from rest_framework.test import APITestCase, APIClient
# from rest_framework import status
# from django.urls import reverse
#
# from .auth import Authentication
# from .models import CustomUser, TemporaryCustomUser
# from django.utils import timezone
# import datetime
#
# class UserAccountTests(APITestCase):
#
#     def setUp(self):
#         # Создаем пользователя для тестирования
#         self.user = CustomUser.objects.create_user(phone_number="+79871620432", password="testpassword")
#         self.client = APIClient()
#
#     def test_verify_token(self):
#         # Вход в систему для получения токена
#         login_response = self.client.post(reverse('login'), {
#             "phone_number": "+79871620432",
#             "password": "testpassword"
#         })
#         login_response_data = login_response.json()
#         access_token = login_response_data.get('access')
#
#         # Проверяем, что токен был получен
#         self.assertIsNotNone(access_token, "Не удалось получить токен доступа")
#
#         # Имитируем аутентифицированный запрос с использованием токена
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
#         response = self.client.get(reverse('balance-list'))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#         # Верификация токена
#         decoded_data = Authentication.verify_token(access_token)
#         self.assertIsNotNone(decoded_data, "Токен не прошел верификацию")
#         self.assertEqual(decoded_data['user_id'], self.user.id, "Токен не соответствует ожидаемому пользователю")
#     # def test_initial_registration(self):
#     #     data = {"phone_number": "+79871620432", "password": "testpassword"}
#     #     response = self.client.post(reverse('register'), data)
#     #     print("Response Data (Initial Registration):", response.data)  # Логирование ответа
#     #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#     #
#     # def test_confirm_registration(self):
#     #     temp_user = TemporaryCustomUser.objects.create(phone_number="+79871620432", temp_token="0432")
#     #     data = {"temp_token": "0432", "code": "1111", "password": "testpassword", "name": "Test User",
#     #             "birthdate": "1990-01-01"}
#     #     response = self.client.post(reverse('register-confirm'), data)
#     #     print("Response Data (Confirm Registration):", response.data)  # Логирование ответа
#     #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#     #
#     # def test_login(self):
#     #     """
#     #     Тестирование процесса входа в систему
#     #     """
#     #     user = CustomUser.objects.create_user(phone_number="+79871620432", password="testpassword")
#     #     data = {
#     #         "phone_number": "+79871620432",
#     #         "password": "testpassword"
#     #     }
#     #     response = self.client.post(reverse('login'), data)
#     #     response_json = response.json()
#     #     self.assertIn("access", response_json)
#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     #
#     # def test_logout(self):
#     #     """
#     #     Тестирование процесса выхода из системы
#     #     """
#     #     user = CustomUser.objects.create_user(phone_number="+79871620432", password="testpassword")
#     #     data = {
#     #         "phone_number": "+79871620432",
#     #         "password": "testpassword"
#     #     }
#     #     login = self.client.post(reverse('login'), data)
#     #     login_response = login.json()
#     #     access_token = login_response.get('access')  # Извлечение токена из ответа
#     #
#     #     # Проверка, получен ли токен
#     #     self.assertIsNotNone(access_token, "Не удалось получить токен")
#     #
#     #     # Использование токена для аутентификации в последующих запросах
#     #     self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
#     #     response = self.client.get(reverse('logout'))
#     #     print("Response Status Code (Logout):", response.status_code)
#     #     print("Response Data (Logout):", response.data)  # Добавлен вывод данных ответа
#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     #
#
#     # def test_refresh_token(self):
#     #     """
#     #     Тестирование обновления токена доступа
#     #     """
#     #     user = CustomUser.objects.create_user(phone_number="+79871620432", password="testpassword")
#     #     data = {
#     #             "phone_number": "+79871620432",
#     #             "password": "testpassword"
#     #     }
#     #     login = self.client.post(reverse('login'), data)
#     #     login_response = login.json()
#     #     # print(login_response)
#     #     refresh_token = login_response.get('refresh')
#     #     access_token = login_response.get('access')  # Извлечение токена из ответа
#     #
#     #     # Проверка, получен ли токен
#     #     self.assertIsNotNone(access_token, "Не удалось получить токен")
#     #
#     #     # Использование токена для аутентификации в последующих запросах
#     #     self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
#     #
#     #     response = self.client.post(reverse('refresh'), {
#     #                                                     'refresh': refresh_token
#     #                                                      })
#     #     # print(response.data)
#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     #     self.assertIn("access", response.data)
#
#     # Добавьте дополнительные тесты для других функций вашего приложения
#
