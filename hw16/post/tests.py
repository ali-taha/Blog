from django.test import TestCase
from django.test.utils import tag
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import *
from django.contrib.auth import get_user_model
from model_mommy import mommy

User = get_user_model()

class TestPostList(APITestCase):
    def setUp(self):
        user1 = User.objects.create(
            username="test",
            password="123",
        )

        mommy.make(Post, is_published=True, writer=user1, _quantity=4)

    def test_post_list(self):
        url = reverse("post_list_api")
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(response.data), 4)
        print(response.json())

    def test_post(self):
        url = reverse("post_api",kwargs={"id":2})
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        print(response.data)
        





   # post1 = Post.objects.create(
    #     writer = user1,
    #     title="post1",
    #     short_description="short_description 1",
    #     description="description  1",
    #     is_published=True,
    # )
    # post2 = Post.objects.create(
    #     writer = user1,
    #     title="post2",
    #     short_description="short_description 2",
    #     description="description  2",
    #     is_published=True,
    # )
    # post3 = Post.objects.create(
    #     writer = user1,
    #     title="post3",
    #     short_description="short_description 3",
    #     description="description  3",
    #     is_published=True,
    # )
    # post4 = Post.objects.create(
    #     writer = user1,
    #     title="post4",
    #     short_description="short_description 4",
    #     description="description  4",
    #     is_published=True,
    # )