from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='NoName')
        cls.user_another = User.objects.create_user(username='I_is_not_NoName')
        cls.group = Group.objects.create(
            title='test-text',
            slug='test-slug',
            description='test_description',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='test-post-text',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client_not_author = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_client_not_author.force_login(self.user_another)

#    def test_home_url_exists_at_desired_location(self):
#        """Страница / доступна любому пользователю."""
#        response = self.guest_client.get('/')
#        self.assertEqual(response.status_code, 200)
#
#    def test_group_url_exists_at_desired_location(self):
#        """Страница group/<slug>/ доступна любому пользователю."""
#        response = self.guest_client.get('/group/test-slug/')
#        self.assertEqual(response.status_code, 200)
#
#    def test_profile_url_exists_at_desired_location(self):
#        """Страница /profile/<username>/ доступна любому пользователю."""
#        response = self.guest_client.get('/profile/NoName/')
#        self.assertEqual(response.status_code, 200)
#
#    def test_post_detail_url_exists_at_desired_location(self):
#        """Страница /posts/<post_id>/ доступна любому
#        пользователю."""
#        response = self.guest_client.get(f'/posts/{self.post.id}/')
#        self.assertEqual(response.status_code, 200)
#
#    def test_post_edit_url_exists_at_desired_location_author(self):
#        """Страница /posts/<post_id>/edit/ доступна автору."""
#        response = self.authorized_client.get(f'/posts/{self.post.id}/edit/')
#        self.assertEqual(response.status_code, 200)
#
#    def test_post_edit_url_forbidden_anonymous(self):
#        """Страница /posts/<post_id>/edit/ перенаправляет анонимного пользователя на страницу регистрации."""
#        response = self.guest_client.get(f'/posts/{self.post.id}/edit/',follow=True)
#        self.assertRedirects(
#            response, (f'/auth/login/?next=/posts/{self.post.id}/edit/')) 
#
#    def test_post_edit_url_forbidden_anoyher_user(self):
#        """Страница /posts/<post_id>/edit/ перенаправляет не автора на страницу поста."""
#        response = self.authorized_client_not_author.get(f'/posts/{self.post.id}/edit/',follow=True)
#        self.assertRedirects(
#            response, (f'/posts/{self.post.id}/'))    
#
#    def test_create_exists_at_desired_location_authorized(self):
#        """Страница /create/ доступна авторизованному пользователю."""
#        response = self.authorized_client.get('/create/')
#        self.assertEqual(response.status_code, 200)
#
#    def test_unexisting_page_url_exists_at_desired_location(self):
#        """Страница /unexisting_page/ не существует."""
#        response = self.guest_client.get('/unexisting_page/')
#        self.assertEqual(response.status_code, 404)   

    def test_url_exists_at_desired_location(self):
        """Страницы доступные любому пользователю."""
        url_names = {
            '/': 200,
            '/group/test-slug/': 200,
            '/profile/NoName/': 200,
            f'/posts/{self.post.id}/': 200,
            '/unexisting_page/': 404,
        }
        for address, status_code in url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, status_code) 

    def test_post_edit_url_exists_at_desired_location_author(self):
        """Страница /posts/<post_id>/edit/ доступна автору."""
        response = self.authorized_client.get(f'/posts/{self.post.id}/edit/')
        self.assertEqual(response.status_code, 200)

    def test_post_edit_url_exists_at_desired_location_author(self):
        """Страница /posts/<post_id>/edit/ перенаправляет не авторов."""
        clients = {
            self.guest_client: f'/auth/login/?next=/posts/{self.post.id}/edit/',
            self.authorized_client_not_author: f'/posts/{self.post.id}/',
        }
        for user_status, redirect in clients.items():
            with self.subTest(user_status=user_status):
                response = user_status.get(f'/posts/{self.post.id}/edit/',follow=True)
                self.assertRedirects(response, redirect)      