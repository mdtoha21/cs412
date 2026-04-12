from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Follow, Photo, Post, Profile


class MiniInstaAPITests(APITestCase):
	def setUp(self):
		self.user_alice = User.objects.create_user(username="apitest_alice", password="password123")
		self.user_bob = User.objects.create_user(username="apitest_bob", password="password123")

		self.alice_profile = Profile.objects.create(username="apitest_alice", display_name="Alice")
		self.bob_profile = Profile.objects.create(username="apitest_bob", display_name="Bob")

		self.bob_post = Post.objects.create(profile=self.bob_profile, caption="hello from bob")
		Photo.objects.create(post=self.bob_post, image_url="https://example.com/bob.jpg")

		Follow.objects.create(profile=self.bob_profile, follower_profile=self.alice_profile)

	def _login(self, username, password="password123"):
		response = self.client.post(
			reverse("api_login"),
			{"username": username, "password": password},
			format="json",
		)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		return response.data["token"], response.data["profile"]["id"]

	def test_login_returns_token_and_profile(self):
		response = self.client.post(
			reverse("api_login"),
			{"username": "apitest_alice", "password": "password123"},
			format="json",
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn("token", response.data)
		self.assertIn("profile", response.data)
		self.assertEqual(response.data["profile"]["username"], "apitest_alice")

	def test_profiles_requires_auth(self):
		response = self.client.get(reverse("api_profiles"))
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_can_read_profiles_with_auth(self):
		token, _ = self._login("apitest_alice")
		self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

		response = self.client.get(reverse("api_profiles"))
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		usernames = {profile["username"] for profile in response.data}
		self.assertIn("apitest_alice", usernames)
		self.assertIn("apitest_bob", usernames)

	def test_my_feed_returns_followed_posts(self):
		token, profile_id = self._login("apitest_alice")
		self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

		Follow.objects.get_or_create(profile=self.bob_profile, follower_profile_id=profile_id)

		response = self.client.get(reverse("api_my_feed"))
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 1)
		self.assertEqual(response.data[0]["caption"], "hello from bob")

	def test_create_post_for_authenticated_user(self):
		token, profile_id = self._login("apitest_alice")
		self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

		response = self.client.post(
			reverse("api_create_post"),
			{
				"caption": "new post from alice",
				"image_url": "https://example.com/alice.jpg",
			},
			format="json",
		)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data["caption"], "new post from alice")
		self.assertEqual(response.data["profile_id"], profile_id)

		created_post = Post.objects.get(pk=response.data["id"])
		self.assertEqual(created_post.profile, self.alice_profile)
		self.assertEqual(created_post.photo_set.count(), 1)
