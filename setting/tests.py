from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from login.models import Avatar
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()
# python manage.py test -v 2

class AvatarUpdateViewTests(TestCase):
    def setUp(self):
        # Create user and avatar instance
        self.avatar = Avatar.objects.create(
            avatarid="crab", 
            image="avatars/crab_k8E25KY.png"
        )
        self.user = User.objects.create_user(
            username="testuser", 
            password="password123", 
            avatar=self.avatar
        )
        self.login_url = reverse('user:login')
        self.avatar_update_url = reverse('setting:avatar-update')

    # アバターアップデートにログインなしでは入れない
    def test_avatar_update_view_access(self):
        """ Test if the avatar update page requires login """
        response = self.client.get(self.avatar_update_url)
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    # アバターの登録ができるか
    def test_avatar_update_post(self):
        """ Test updating an avatar successfully """
        self.client.login(username='testuser', password='password123')
        # Simulate an image file upload  AdobeStock_252443785.jpeg
        with open("C:/Users/konno/Downloads/cat.png", 'rb') as img:
            image = SimpleUploadedFile(img.name, img.read(), content_type='image/png')

        response = self.client.post(self.avatar_update_url, {
            'avatarid': 'new_avatar',
            'image': image,
        })
        self.assertRedirects(response, reverse('setting:home'))

        updated_avatar = Avatar.objects.get(avatarid='new_avatar')
        self.assertTrue(updated_avatar.image.name.startswith('avatars/cat'))

class SettingUpdateViewTests(TestCase):
    def setUp(self):
        # Create a user and an avatar instance
        self.avatar = Avatar.objects.create(
            avatarid="crab", 
            image="avatars/crab_k8E25KY.png"
        )
        self.user = User.objects.create_user(
            username="testuser", 
            password="password123", 
            avatar=self.avatar
        )
        self.login_url = reverse('user:login')
        self.setting_update_url = reverse('setting:setting-update', kwargs={'pk': self.user.pk})
    
    # セッティングにはログインが必要
    def test_setting_update_view_access(self):
        """ Test if the setting update page requires login """
        response = self.client.get(self.setting_update_url)
        self.assertEqual(response.status_code, 302)  # Should redirect to login
    
    # セッティングにはアップデート可能
    def test_setting_update_post(self):
        """ Test updating user settings (username, avatar) """
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.setting_update_url, {
            'username': 'updateduser',
            'avatar': self.avatar.pk,
        })
        self.assertRedirects(response, reverse('setting:home'))

        updated_user = User.objects.get(pk=self.user.pk)
        self.assertEqual(updated_user.username, 'updateduser')