from django.test import TestCase
from app.models import User, Event, Comment
from django.utils import timezone
from django.contrib.auth import get_user_model
import datetime


class TestCommentCreation(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpass'
        )
        self.event = Event.objects.create(
            title="Evento de prueba",
            description="Descripción del evento",
            date=timezone.now() + datetime.timedelta(days=1)
        )

    def test_create_comment_valid(self):
        success, comment = Comment.new(
            user=self.user,
            event=self.event,
            title="Buen evento",
            text="Me gustó mucho"
        )
        self.assertTrue(success)
        self.assertIsInstance(comment, Comment)
        self.assertEqual(comment.title, "Buen evento")
        self.assertEqual(comment.text, "Me gustó mucho")
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.event, self.event)

    def test_create_comment_invalid_empty_fields(self):
        success, errors = Comment.new(
            user=self.user,
            event=self.event,
            title="",
            text=""
        )
        self.assertFalse(success)
        self.assertIn("title", errors)
        self.assertIn("text", errors)

class TestCommentValidation(TestCase):

    def test_validate_comment_empty_title(self):
        errors = Comment.validate(title="", text="Comentario cualquiera")
        self.assertIn("title", errors)
        self.assertNotIn("text", errors)

    def test_validate_comment_empty_text(self):
        errors = Comment.validate(title="Título cualquiera", text="")
        self.assertIn("text", errors)
        self.assertNotIn("title", errors)

    def test_validate_comment_empty_title_and_text(self):
        errors = Comment.validate(title="", text="")
        self.assertIn("title", errors)
        self.assertIn("text", errors)

    def test_validate_comment_valid_data(self):
        errors = Comment.validate(title="Título", text="Texto del comentario")
        self.assertEqual(errors, {})

class TestCommentUpdate(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpass'
        )
        self.event = Event.objects.create(
            title="Evento de prueba",
            description="Descripción del evento",
            date=timezone.now() + datetime.timedelta(days=1)
        )
        _, self.comment = Comment.new(
            user=self.user,
            event=self.event,
            title="Título inicial",
            text="Texto inicial"
        )

    def test_update_comment_title(self):
        self.comment.update(title="Nuevo título")
        updated = Comment.objects.get(pk=self.comment.pk)
        self.assertEqual(updated.title, "Nuevo título")
        self.assertEqual(updated.text, "Texto inicial")

    def test_update_comment_text(self):
        self.comment.update(text="Nuevo texto")
        updated = Comment.objects.get(pk=self.comment.pk)
        self.assertEqual(updated.title, "Título inicial")
        self.assertEqual(updated.text, "Nuevo texto")

    def test_update_comment_both_fields(self):
        self.comment.update(title="Nuevo título", text="Nuevo texto")
        updated = Comment.objects.get(pk=self.comment.pk)
        self.assertEqual(updated.title, "Nuevo título")
        self.assertEqual(updated.text, "Nuevo texto")

    def test_update_comment_no_changes(self):
        self.comment.update()
        updated = Comment.objects.get(pk=self.comment.pk)
        self.assertEqual(updated.title, "Título inicial")
        self.assertEqual(updated.text, "Texto inicial")