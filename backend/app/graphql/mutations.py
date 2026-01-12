import strawberry
from typing import Optional
from graphql import GraphQLError
from .types import CommentType
from app.comments.models import Comment


@strawberry.type
class Mutation:
    """GraphQL мутации для работы с комментариями"""

    @strawberry.mutation
    def create_comment(
            self,
            info,
            text: str,
            reply_id: Optional[int] = None
    ) -> CommentType:
        """
        Создание нового комментария

        Args:
            info: GraphQL context (содержит request с пользователем)
            text: Текст комментария
            reply_id: ID родительского комментария (для ответов)

        Returns:
            Созданный комментарий

        Raises:
            GraphQLError: Чистая ошибка без traceback
        """
        user = info.context.request.user

        if not user.is_authenticated:
            raise GraphQLError(
                "Требуется авторизация!",
                extensions={"code": "UNAUTHORIZED"}
            )

        reply = None
        if reply_id:
            try:
                reply = Comment.objects.get(id=reply_id)
            except Comment.DoesNotExist:
                raise GraphQLError(
                    f"Комментарий с ID {reply_id} не найден",
                    extensions={"code": "NOT_FOUND"}
                )

        comment = Comment.objects.create(
            user=user,
            text=text,
            reply=reply
        )

        return comment

    @strawberry.mutation
    def update_comment(
            self,
            info,
            comment_id: int,
            text: str
    ) -> CommentType:
        """
        Обновление существующего комментария

        Args:
            info: GraphQL context
            comment_id: ID комментария для обновления
            text: Новый текст комментария

        Returns:
            Обновленный комментарий

        Raises:
            GraphQLError: Чистая ошибка без traceback
        """
        user = info.context.request.user

        if not user.is_authenticated:
            raise GraphQLError(
                "Требуется авторизация!",
                extensions={"code": "UNAUTHORIZED"}
            )

        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            raise GraphQLError(
                f"Комментарий с ID {comment_id} не найден",
                extensions={"code": "NOT_FOUND"}
            )

        if comment.user != user:
            raise GraphQLError(
                "Вы можете редактировать только свои комментарии!",
                extensions={"code": "FORBIDDEN"}
            )

        comment.text = text
        comment.save()

        return comment

    @strawberry.mutation
    def delete_comment(
            self,
            info,
            comment_id: int
    ) -> bool:
        """
        Удаление комментария

        Args:
            info: GraphQL context
            comment_id: ID комментария для удаления

        Returns:
            True если успешно удален

        Raises:
            GraphQLError: Чистая ошибка без traceback
        """
        user = info.context.request.user

        if not user.is_authenticated:
            raise GraphQLError(
                "Требуется авторизация!",
                extensions={"code": "UNAUTHORIZED"}
            )

        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            raise GraphQLError(
                f"Комментарий с ID {comment_id} не найден",
                extensions={"code": "NOT_FOUND"}
            )

        if comment.user != user:
            raise GraphQLError(
                "Вы можете удалять только свои комментарии!",
                extensions={"code": "FORBIDDEN"}
            )

        comment.delete()

        return True