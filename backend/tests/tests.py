"""
Полный набор тестов для CommentHub
Переписано с нуля с учетом всех зависимостей
"""
import json
from unittest.mock import patch, MagicMock

from django.test import TestCase, override_settings, TransactionTestCase
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core import mail

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async

from app.comments.models import Comment
from app.comments.consumers import ReplyConsumer
from app.comments.serializers import CommentSerializer, CommentCreateSerializer
import app.comments.signals  # Явно импортируем сигналы для тестов

User = get_user_model()


# ============================================
# БАЗОВЫЙ КЛАСС С ОБЩИМИ МОКАМИ
# ============================================
class BaseTestCase:
    """Базовый класс с настройкой общих моков"""

    def setUp(self):
        super().setUp()
        # Mock для reCAPTCHA во всех тестах
        self.recaptcha_patcher = patch('app.comments.serializers.requests.post')
        self.mock_recaptcha = self.recaptcha_patcher.start()
        self.mock_recaptcha.return_value = MagicMock(
            json=lambda: {"success": True}
        )

        # Очищаем кеш перед каждым тестом
        cache.clear()

        # Очищаем почтовый ящик
        mail.outbox = []

    def tearDown(self):
        super().tearDown()
        self.recaptcha_patcher.stop()
        cache.clear()


# ============================================
# ТЕСТЫ МОДЕЛЕЙ
# ============================================
class UserModelTest(TestCase):
    """Тесты модели User"""

    def test_create_user(self):
        """Создание пользователя"""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))

    def test_user_string_representation(self):
        """Строковое представление пользователя"""
        user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.assertEqual(str(user), "testuser")


class CommentModelTest(TestCase):
    """Тесты модели Comment"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

    def test_create_comment(self):
        """Создание комментария"""
        comment = Comment.objects.create(
            user=self.user,
            text="Test comment"
        )
        self.assertEqual(comment.text, "Test comment")
        self.assertEqual(comment.user, self.user)
        self.assertIsNone(comment.reply)

    def test_create_reply(self):
        """Создание ответа на комментарий"""
        parent = Comment.objects.create(
            user=self.user,
            text="Parent comment"
        )
        reply = Comment.objects.create(
            user=self.user,
            text="Reply comment",
            reply=parent
        )
        self.assertEqual(reply.reply, parent)
        self.assertIn(reply, parent.replies.all())

    def test_get_root_comment(self):
        """Получение корневого комментария"""
        root = Comment.objects.create(
            user=self.user,
            text="Root"
        )
        reply1 = Comment.objects.create(
            user=self.user,
            text="Reply 1",
            reply=root
        )
        reply2 = Comment.objects.create(
            user=self.user,
            text="Reply 2",
            reply=reply1
        )

        self.assertEqual(reply2.get_root_comment(), root)
        self.assertEqual(reply1.get_root_comment(), root)
        self.assertEqual(root.get_root_comment(), root)

    def test_comment_timestamps(self):
        """Автоматические временные метки"""
        comment = Comment.objects.create(
            user=self.user,
            text="Test"
        )
        self.assertIsNotNone(comment.created_at)
        self.assertIsNotNone(comment.updated_at)


# ============================================
# ТЕСТЫ СЕРИАЛИЗАТОРОВ
# ============================================
class CommentSerializerTest(BaseTestCase, TestCase):
    """Тесты сериализаторов комментариев"""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

    def test_comment_serializer(self):
        """Сериализация комментария"""
        comment = Comment.objects.create(
            user=self.user,
            text="Test comment"
        )
        serializer = CommentSerializer(comment)
        data = serializer.data

        self.assertEqual(data["text"], "Test comment")
        self.assertEqual(data["user"]["username"], "testuser")
        self.assertIn("id", data)
        self.assertIn("created_at", data)
        self.assertIn("replies", data)

    def test_html_sanitization(self):
        """Санитизация опасного HTML"""
        serializer = CommentCreateSerializer(
            data={
                "text": "<script>alert('xss')</script>Hello <strong>World</strong>",
                "recaptcha_token": "test-token"
            }
        )
        self.assertTrue(serializer.is_valid())

        # Скрипт удален, разрешенные теги остались
        validated_text = serializer.validated_data["text"]
        self.assertNotIn("<script>", validated_text)
        self.assertIn("Hello", validated_text)
        self.assertIn("<strong>", validated_text)

    def test_allowed_html_tags(self):
        """Разрешенные HTML теги"""
        text = '<a href="http://example.com">Link</a> <strong>Bold</strong> <code>Code</code>'
        serializer = CommentCreateSerializer(
            data={"text": text, "recaptcha_token": "test-token"}
        )
        self.assertTrue(serializer.is_valid())

        validated_text = serializer.validated_data["text"]
        self.assertIn("<a", validated_text)
        self.assertIn("<strong>", validated_text)
        self.assertIn("<code>", validated_text)


# ============================================
# ТЕСТЫ API
# ============================================
class CommentAPITest(BaseTestCase, APITestCase):
    """Тесты API комментариев"""

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

    def test_list_comments_unauthorized(self):
        """Получение списка без авторизации"""
        response = self.client.get("/api/comments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_comments_authorized(self):
        """Получение списка с авторизацией"""
        Comment.objects.create(user=self.user, text="Test")

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.get("/api/comments/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем с учетом пагинации
        if isinstance(response.data, dict) and 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
        else:
            self.assertEqual(len(response.data), 1)

    def test_create_comment_unauthorized(self):
        """Создание комментария без авторизации"""
        response = self.client.post(
            "/api/comments/",
            {"text": "New comment", "recaptcha_token": "test-token"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_comment_authorized(self):
        """Создание комментария с авторизацией"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.post(
            "/api/comments/",
            {"text": "New comment", "recaptcha_token": "test-token"}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().text, "New comment")

    def test_create_reply(self):
        """Создание ответа на комментарий"""
        parent = Comment.objects.create(user=self.user, text="Parent")

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.post(
            "/api/comments/",
            {
                "text": "Reply",
                "reply": parent.id,
                "recaptcha_token": "test-token"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)

        reply = Comment.objects.get(text="Reply")
        self.assertEqual(reply.reply, parent)

    def test_update_comment(self):
        """Обновление комментария"""
        comment = Comment.objects.create(user=self.user, text="Original")

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.patch(
            f"/api/comments/{comment.id}/",
            {"text": "Updated", "recaptcha_token": "test-token"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        comment.refresh_from_db()
        self.assertEqual(comment.text, "Updated")

    def test_delete_comment(self):
        """Удаление комментария"""
        comment = Comment.objects.create(user=self.user, text="Test")

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.delete(f"/api/comments/{comment.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

    def test_only_top_level_in_list(self):
        """В списке только комментарии верхнего уровня"""
        parent = Comment.objects.create(user=self.user, text="Parent")
        Comment.objects.create(user=self.user, text="Reply", reply=parent)

        response = self.client.get("/api/comments/")

        if isinstance(response.data, dict) and 'results' in response.data:
            results = response.data['results']
        else:
            results = response.data

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["text"], "Parent")


# ============================================
# ТЕСТЫ WEBSOCKET
# ============================================
class WebSocketTest(TestCase):
    """Тесты WebSocket consumer"""

    async def test_connect_unauthorized(self):
        """Подключение без авторизации"""
        communicator = WebsocketCommunicator(
            ReplyConsumer.as_asgi(),
            "/ws/comments/1/"
        )
        communicator.scope["user"] = None

        connected, _ = await communicator.connect()
        self.assertFalse(connected)

    async def test_connect_authorized(self):
        """Подключение с авторизацией"""
        user = await database_sync_to_async(User.objects.create_user)(
            username="testuser",
            password="testpass123"
        )

        communicator = WebsocketCommunicator(
            ReplyConsumer.as_asgi(),
            "/ws/comments/1/"
        )
        communicator.scope["user"] = user
        communicator.scope["url_route"] = {"kwargs": {"comment_name": "1"}}

        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        await communicator.disconnect()

    async def test_receive_reply_notification(self):
        """Получение уведомления о новом ответе"""
        user = await database_sync_to_async(User.objects.create_user)(
            username="testuser",
            password="testpass123"
        )

        communicator = WebsocketCommunicator(
            ReplyConsumer.as_asgi(),
            "/ws/comments/1/"
        )
        communicator.scope["user"] = user
        communicator.scope["url_route"] = {"kwargs": {"comment_name": "1"}}

        await communicator.connect()

        # Отправляем уведомление
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            "comment_1",
            {
                "type": "new_reply",
                "reply": {"id": 1, "text": "Test reply"}
            }
        )

        # Получаем сообщение
        response = await communicator.receive_from()
        data = json.loads(response)

        self.assertEqual(data["type"], "new_reply")
        self.assertEqual(data["data"]["text"], "Test reply")

        await communicator.disconnect()


# ============================================
# ТЕСТЫ EMAIL УВЕДОМЛЕНИЙ
# ============================================
class EmailNotificationTest(BaseTestCase, APITestCase):
    """Тесты email уведомлений"""

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username="user1",
            email="user1@example.com",
            password="pass123"
        )
        self.user2 = User.objects.create_user(
            username="user2",
            email="user2@example.com",
            password="pass123"
        )
        self.token = str(RefreshToken.for_user(self.user2).access_token)

    def test_email_sent_on_reply(self):
        """Email отправляется при ответе"""
        parent = Comment.objects.create(user=self.user1, text="Parent")

        with patch("app.comments.tasks.send_reply_notification_email.delay") as mock:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
            response = self.client.post(
                "/api/comments/",
                {
                    "text": "Reply",
                    "reply": parent.id,
                    "recaptcha_token": "test-token"
                }
            )

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            mock.assert_called_once()

            call_kwargs = mock.call_args[1]
            self.assertEqual(call_kwargs["user_email"], "user1@example.com")
            self.assertIn("Reply", call_kwargs["comment_text_short"])

    def test_email_not_sent_to_self(self):
        """Email не отправляется самому себе"""
        parent = Comment.objects.create(user=self.user1, text="Parent")
        token = str(RefreshToken.for_user(self.user1).access_token)

        with patch("app.comments.tasks.send_reply_notification_email.delay") as mock:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
            self.client.post(
                "/api/comments/",
                {
                    "text": "Self reply",
                    "reply": parent.id,
                    "recaptcha_token": "test-token"
                }
            )

            mock.assert_not_called()

    def test_email_task_execution(self):
        """Выполнение задачи отправки email"""
        from app.comments.tasks import send_reply_notification_email

        send_reply_notification_email(
            user_email="test@example.com",
            comment_text_short="Test reply"
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["test@example.com"])
        self.assertIn("Новый ответ", mail.outbox[0].subject)
        self.assertIn("Test reply", mail.outbox[0].body)


# ============================================
# ТЕСТЫ КЕШИРОВАНИЯ
# ============================================
class CachingTest(BaseTestCase, APITestCase):
    """Тесты Redis кеширования (с локальным кешем в тестах)"""

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.token = str(RefreshToken.for_user(self.user).access_token)

    def test_preview_caching(self):
        """Кеширование preview списка"""
        Comment.objects.create(user=self.user, text="Test 1")

        # Первый запрос - из БД
        response1 = self.client.get("/api/comments/preview/")
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

        # Проверяем что закешировано
        cached = cache.get("comment_preview_list")
        self.assertIsNotNone(cached)

        # Второй запрос - из кеша
        response2 = self.client.get("/api/comments/preview/")
        self.assertEqual(response1.data, response2.data)

    def test_cache_invalidation(self):
        """Инвалидация кеша при создании комментария"""
        # Создаем первый комментарий
        Comment.objects.create(user=self.user, text="Comment 1")

        # Кешируем данные
        response1 = self.client.get("/api/comments/preview/")
        self.assertEqual(len(response1.data), 1)

        # Проверяем что данные закешированы
        self.assertIsNotNone(cache.get("comment_preview_list"))

        # Вручную создаем второй комментарий (что должно очистить кеш через сигнал)
        Comment.objects.create(user=self.user, text="Comment 2")

        # ВАЖНО: В тестах с TestCase сигналы работают внутри транзакции,
        # поэтому проверяем, что API возвращает актуальные данные
        response2 = self.client.get("/api/comments/preview/")
        self.assertEqual(
            len(response2.data),
            2,
            "API should return fresh data after new comment is created"
        )

    def test_only_top_level_cached(self):
        """Кешируются только комментарии верхнего уровня"""
        parent = Comment.objects.create(user=self.user, text="Parent")
        Comment.objects.create(user=self.user, text="Reply", reply=parent)

        response = self.client.get("/api/comments/preview/")

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["text"], "Parent")