# from rest_framework.test import APITestCase
# from .views import get_random, get_access_token, get_refresh_token
# from .models import CustomUser, UserProfile
#
#
# class TestGenericFunctions(APITestCase):
#
#     def test_get_random(self):
#
#         rand1 = get_random(10)
#         rand2 = get_random(10)
#         rand3 = get_random(15)
#
#         # check that we are getting a result
#         self.assertTrue(rand1)
#
#         # check that rand1 is not equal to rand2
#         self.assertNotEqual(rand1, rand2)
#
#         # check that the length of result is what is expected
#         self.assertEqual(len(rand1), 10)
#         self.assertEqual(len(rand3), 15)
#
#     def test_get_access_token(self):
#         payload = {
#             "id": 1
#         }
#
#         token = get_access_token(payload)
#
#         # check that we obtained a result
#         self.assertTrue(token)
#
#     def test_get_refresh_token(self):
#
#         token = get_refresh_token()
#
#         # check that we obtained a result
#         self.assertTrue(token)
#
#
# class TestAuth(APITestCase):
#     login_url = "/auth/login"
#     register_url = "/auth/register"
#     refresh_url = "/auth/refresh"
#
#     def test_register(self):
#         payload = {
#             "username": "adefemigreat",
#             "password": "ade123",
#             "email": "adefemigreat@yahoo.com"
#         }
#
#         response = self.client.post(self.register_url, data=payload)
#
#         # check that we obtain a status of 201
#         self.assertEqual(response.status_code, 201)
#
#     def test_login(self):
#         payload = {
#             "username": "adefemigreat",
#             "password": "ade123",
#             "email": "adefemigreat@yahoo.com"
#         }
#
#         # register
#         self.client.post(self.register_url, data=payload)
#
#         # login
#         response = self.client.post(self.login_url, data=payload)
#         result = response.json()
#
#         # check that we obtain a status of 200
#         self.assertEqual(response.status_code, 200)
#
#         # check that we obtained both the refresh and access token
#         self.assertTrue(result["access"])
#         self.assertTrue(result["refresh"])
#
#     def test_refresh(self):
#         payload = {
#             "username": "adefemigreat",
#             "password": "ade123",
#             "email": "adefemigreat@yahoo.com"
#         }
#
#         # register
#         self.client.post(self.register_url, data=payload)
#
#         # login
#         response = self.client.post(self.login_url, data=payload)
#         refresh = response.json()["refresh"]
#
#         # get refresh
#         response = self.client.post(
#             self.refresh_url, data={"refresh": refresh})
#         result = response.json()
#
#         # check that we obtain a status of 200
#         self.assertEqual(response.status_code, 200)
#
#         # check that we obtained both the refresh and access token
#         self.assertTrue(result["access"])
#         self.assertTrue(result["refresh"])
#
#
# class TestUserInfo(APITestCase):
#     profile_url = "/auth/profile"
#     login_url = "/auth/login"
#
#     def setUp(self):
#         payload = {
#             "username": "adefemigreat",
#             "password": "ade123",
#             "email": "adefemigreat@yahoo.com"
#         }
#
#         self.user = CustomUser.objects.create_user(**payload)
#
#         # login
#         response = self.client.post(self.login_url, data=payload)
#         result = response.json()
#
#         self.bearer = {
#             'HTTP_AUTHORIZATION': 'Bearer {}'.format(result['access'])}
#
#
#     def test_user_search(self):
#
#         UserProfile.objects.create(user=self.user, first_name="Adefemi", last_name="oseni",
#                                    caption="live is all about living", about="I'm a youtuber")
#
#         user2 = CustomUser.objects.create_user(
#             username="tester", password="tester123", email="adefemi@yahoo.com")
#         UserProfile.objects.create(user=user2, first_name="Vester", last_name="Mango",
#                                    caption="it's all about testing", about="I'm a youtuber")
#
#         user3 = CustomUser.objects.create_user(
#             username="vasman", password="vasman123", email="adefemi@yahoo.com2")
#         UserProfile.objects.create(user=user3, first_name="Adeyemi", last_name="Boseman",
#                                    caption="it's all about testing", about="I'm a youtuber")
#
#         # test keyword = adefemi oseni
#         url = self.profile_url + "?keyword=adefemi oseni"
#
#         response = self.client.get(url, **self.bearer)
#         result = response.json()["results"]
#
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(result), 0)
#
#         # test keyword = ade
#         url = self.profile_url + "?keyword=ade"
#
#         response = self.client.get(url, **self.bearer)
#         result = response.json()["results"]
#
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(result), 2)
#         self.assertEqual(result[1]["user"]["username"], "vasman")
#
#         # test keyword = vester
#         url = self.profile_url + "?keyword=vester"
#
#         response = self.client.get(url, **self.bearer)
#         result = response.json()["results"]
#
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(result), 1)
#         self.assertEqual(result[0]["user"]["username"], "tester")