from datetime import timedelta

from django.utils.timezone import now
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from account.models import Account


class AccountAPITestIntegrated(APITestCase):
    def setUp(self):
        self.signup_url = reverse('signup')  # e.g. /api/account/signup/
        self.login_url = reverse('login')  # e.g. /api/account/login/
        self.verify_otp_url = reverse('verify-otp')
        self.logout_url = reverse('logout')
        self.account_update_url = reverse('account_update')
        self.me_url = reverse('user_detail')

        self.user_data = {
            "username": "testuser",
            "password": "StrongPass123!",
            "email": "test@example.com",
            "first_name": "Mmd",
            "last_name": "Zare",
            "account": {
                "phone_number": "123456789"
            }
        }

        self.existing_user = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='password123'
        )
        self.existing_account = Account.objects.create(
            user=self.existing_user,
            phone_number='1234567890'
        )

        self.client = APIClient()

    def test_full_flow(self):
        """
        This test goes through:
         1) Sign-up
         2) Login (get OTP)
         3) Verify OTP
         4) Get user detail
         5) Update account
         6) Logout
        """

        # 1) Sign up
        response = self.client.post(self.signup_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.data)
        self.assertIn('id', response.data)
        self.assertIn('account', response.data)
        self.assertEqual(response.data['username'], self.user_data['username'])
        self.assertEqual(response.data['email'], self.user_data['email'])

        user = User.objects.filter(username=self.user_data['username']).first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))

        # 2) Login (generates OTP and sends email)
        login_data = {
            "username": self.user_data['username'],
            "password": self.user_data['password']
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertIn('message', response.data)

        # Get OTP from the database
        user.refresh_from_db()
        account = user.account
        self.assertIsNotNone(account.otp)
        self.assertIsNotNone(account.otp_expiry)
        self.assertGreater(account.otp_expiry, timezone.now())

        # 3) Verify OTP
        verify_data = {
            "username": self.user_data['username'],
            "otp": account.otp
        }
        response = self.client.post(self.verify_otp_url, verify_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertIn('message', response.data)
        self.assertIn('phone_number', response.data)
        self.assertEqual(response.data['phone_number'], self.user_data['account']['phone_number'])

        # 4) Get user detail
        response = self.client.get(self.me_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertIn('username', response.data)
        self.assertEqual(response.data['username'], self.user_data['username'])
        self.assertIn('account', response.data)
        self.assertIn('phone_number', response.data['account'])
        self.assertEqual(response.data['account']['phone_number'], self.user_data['account']['phone_number'])

        # 5) Update account
        update_data = {
            "phone_number": "987654321",
            "bio": "New bio content"
        }
        response = self.client.put(self.account_update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['phone_number'], update_data['phone_number'])
        self.assertEqual(response.data['bio'], update_data['bio'])
        self.assertIsNone(response.data['address'])  # since we didn't set it

        account.refresh_from_db()
        self.assertEqual(account.phone_number, "987654321")
        self.assertEqual(account.bio, "New bio content")

        # 6) Logout
        response = self.client.post(self.logout_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertIn('message', response.data)

        response = self.client.get(self.me_url, format='json')
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_signup(self):
        response = self.client.post(self.signup_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('username', response.data)

    def test_login(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser2',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_invalid_login(self):
        response = self.client.post(self.login_url, {
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_otp_verification(self):
        self.existing_account.otp = '123456'
        self.existing_account.otp_expiry = now() + timedelta(minutes=3)
        self.existing_account.save()

        response = self.client.post(self.verify_otp_url, {
            'username': 'testuser2',
            'otp': '123456'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_invalid_otp(self):
        response = self.client.post(self.verify_otp_url, {
            'username': 'testuser2',
            'otp': '999999'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout(self):
        self.client.force_authenticate(user=self.existing_user)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_user_detail_authenticated(self):
        self.client.force_authenticate(user=self.existing_user)
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('username', response.data)
        self.assertEqual(response.data['username'], 'testuser2')

    def test_user_detail_unauthenticated(self):
        response = self.client.get(self.me_url)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_account_update(self):
        self.client.force_authenticate(user=self.existing_user)
        response = self.client.put(self.account_update_url, {
            'bio': 'Updated bio',
            'address': 'New Address'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bio'], 'Updated bio')
        self.assertEqual(response.data['address'], 'New Address')
