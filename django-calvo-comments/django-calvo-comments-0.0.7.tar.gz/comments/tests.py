from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .models import Post, CommentPost
from .forms import PostForm,CommentPostForm


class PostTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="admin")
        CommentPost.objects.create(author=self.user1,
                            title="Test",
                            text="We are testing this",
                            created_date=timezone.now(),
                            published_date=timezone.now())

    def test_post_is_posted(self):
        """Posts are created"""
        post1 = CommentPost.objects.get(title="Test")
        self.assertEqual(post1.text, "We are testing this")

    def test_valid_form_data(self):
        form = CommentPostForm({
            'title': "Just testing",
            'text': "Repeated tests make the app foul-proof",
        })
        self.assertTrue(form.is_valid())
        post1 = form.save(commit=False)
        post1.author = self.user1
        post1.save()
        self.assertEqual(post1.title, "Just testing")
        self.assertEqual(post1.text, "Repeated tests make the app foul-proof")

    def test_blank_form_data(self):
        form = CommentPostForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'title': ['This field is required.'],
            'text': ['This field is required.'],
        })
