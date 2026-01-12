import strawberry
from strawberry import auto
from typing import List, Optional
from app.comments.models import Comment, CommentAttachment
from app.users.models import User


@strawberry.django.type(User)
class UserType:
    """Тип пользователя для GraphQL"""
    id: auto
    username: auto
    email: auto


@strawberry.django.type(CommentAttachment)
class AttachmentType:
    """Тип вложения для GraphQL"""
    id: auto
    file: auto
    media_type: auto


@strawberry.django.type(Comment)
class CommentType:
    """Тип комментария для GraphQL"""
    id: auto
    text: auto
    created_at: auto
    updated_at: auto
    user: UserType

    @strawberry.field
    def reply_id(self) -> Optional[int]:
        """ID родительского комментария"""
        return self.reply.id if self.reply else None

    @strawberry.field
    def short_text(self) -> str:
        """Укороченный текст комментария (первые 50 символов)"""
        return self.text[:50] + "..." if len(self.text) > 50 else self.text

    @strawberry.field
    def reply_list(self) -> List["CommentType"]:
        """
        Список ответов на этот комментарий
        """
        return list(self.replies.all())

    @strawberry.field
    def attachments_list(self) -> List[AttachmentType]:
        """
        Список вложений комментария
        """
        return list(self.attachments.all())

    @strawberry.field
    def reply_count(self) -> int:
        """Количество ответов на комментарий"""
        return self.replies.count()

    @strawberry.field
    def has_attachments(self) -> bool:
        """Есть ли вложения у комментария"""
        return self.attachments.exists()