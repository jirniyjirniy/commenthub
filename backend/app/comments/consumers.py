import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ReplyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Проверка аутентификации
        user = self.scope.get("user")
        if not user or user.is_anonymous:
            print(f"❌ WebSocket rejected: User not authenticated")
            await self.close(code=4001)  # Unauthorized
            return

        # Получаем ID комментария из URL
        self.comment_id = self.scope["url_route"]["kwargs"]["comment_name"]
        self.room_group_name = f"comment_{self.comment_id}"

        # Присоединяемся к группе
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        
        print(f"✅ WebSocket connected: user={user.username}, comment={self.comment_id}")

    async def disconnect(self, close_code):
        # Безопасная отписка (только если connect завершился успешно)
        if hasattr(self, "room_group_name") and hasattr(self, "comment_id"):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
            print(f"🔌 WebSocket disconnected: comment={self.comment_id}, code={close_code}")
        else:
            print(f"🔌 WebSocket disconnected early: code={close_code}")

    async def new_reply(self, event):
        """Отправляет новый ответ всем подключенным клиентам"""
        reply_data = event["reply"]
        await self.send(
            text_data=json.dumps({"type": "new_reply", "data": reply_data})
        )
        print(f"📨 Sent reply notification for comment {self.comment_id}")
