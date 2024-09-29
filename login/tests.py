from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from .models import Avatar
from django.core.files.uploadedfile import SimpleUploadedFile
import os
User = get_user_model()  # Get the custom user model


# Create your tests here.
# python manage.py test -v 2

class UserLoginTests(TestCase):

    def setUp(self):
        # create a test user
        avatar = Avatar.objects.create(
            # id=1,
            avatarid='crab', 
            image='avatars/crab_k8E25KY.png')
        self.user = User.objects.create_user(
            username='testuser', 
            email='testuser@example.com', 
            password='password1234', 
            avatar=avatar
            )
        self.login_url = reverse('user:login')
        self.home_url = reverse('setting:home')
    
    # ログイン画面をロードできるか
    def test_login_view_status_code(self):
        """ Test if the login page loads successfully """
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    # ログインした後,settingのurlに行くかを確認
    def test_login_successful(self):
        """ Test if a user can log in with valid credentials """
        self.response = self.client.post(self.login_url, {
            'username':'testuser',
            'password': 'password1234',
        })
        self.assertRedirects(self.response, self.home_url)
    
    # 間違えのパスワードでログインをした場合
    def test_login_invalid_credentials(self):
        """ Test if a user cannot log in with invalid credentials """
        response = self.client.post(self.login_url, {
            'username':'testuser',
            'password': 'wrongpass',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '正しいユーザー名とパスワードを入力してください')
    
    # すでにログインしているユーザーは、ログイン後の画面に自動的に誘導されるか
    def test_login_redirect_authenticated_user(self):
        """ Test if an authenticated user is redirected when trying to acces the login page """
        self.client.login(username='testuser', password='password1234') #login by this code
        response = self.client.get(self.login_url)                      # get the login-page if automatically redirect to home_url
        self.assertRedirects(response, self.home_url)

class UserRegistrationTests(TestCase):

    def setUp(self):
        self.register_url = reverse('user:register')
        self.login_url = reverse('user:login')
        self.avatar = Avatar.objects.create(id=1)

    # 登録ページを読み込めるか
    def test_registration_view_status_code(self):
        """ Test if the registration page loads successfully """
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
    
    # 新規ユーザーを登録して、そのユーザーがデータベースに反映されているか
    def test_user_registration(self):
        """ Test if a user can register successfully """
        response = self.client.post(self.register_url, {
            'username':'newuser',
            'email': 'newuser@example.com',
            'password1':'password9876',
            'password2':'password9876',
        })
        self.assertRedirects(response, self.login_url)
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    # 同じユーザーははじかれるか？
    def test_user_registration_invalid_data(self):
        """ Test registration with invalid data (e.g. duplicate username) """
        User.objects.create_user(username='newuser', email="another@example.com", password='password9876')
        response = self.client.post(self.register_url, {
            'username':'newuser',
            'email': 'diff@example.com',
            'password1':'password9876',
            'password2':'password9876',
        })
        self.assertEqual(response.status_code, 200)  # Expecting a 200 for invalid registration
        self.assertContains(response, 'This username is already taken')

    # 同じEMAILははじかれるか？
    def test_EMAIL_registration_invalid_data(self):
        """ Test registration with invalid data (e.g. duplicate EMAIL) """
        User.objects.create_user(username='newuser', email="another@example.com", password='password9876')
        response = self.client.post(self.register_url, {
            'username':'diff',
            'email': 'another@example.com',
            'password1':'password9876',
            'password2':'password9876',
        })
        self.assertEqual(response.status_code, 200)  # Expecting a 200 for invalid registration
        self.assertContains(response, 'An account with this email already exists')

class PasswordResetTests(TestCase):

    def setUp(self):
        avatar = Avatar.objects.create(
            # id=1,
            avatarid='crab', 
            image='avatars/crab_k8E25KY.png')
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password123', avatar=avatar)
        self.password_reset_url = reverse_lazy('user:password_reset')
        self.password_reset_done_url = reverse_lazy('user:password_reset_done')

    # パスワードリセットのページにいけるか
    def testpassword_reset_view_status_code(self):
        """ Test if the password reset page loads successfully """
        response = self.client.get(self.password_reset_url)
        self.assertEqual(response.status_code, 200)
    
    # メールを送信できるか
    def test_password_reset_post(self):
        """ Test if passowrd reset email is sent successfully """
        response = self.client.post(self.password_reset_url, {
            'email': 'testuser@example.com',
        })
        self.assertRedirects(response, self.password_reset_done_url)

    # 登録していないメールアドレスを検知できるか
    def test_password_reset_invalid_email(self):
        """ Test if invalid email submission shows correct error message """
        response = self.client.post(self.password_reset_url, {
            'email': 'invalid@example.com',
        })
        self.assertRedirects(response, self.password_reset_done_url)
        # self.assertContains(response, 'An account with this email already exists.')