import strawberry
from typing import List, Optional
from graphql import GraphQLError

from .mutations import Mutation
from .types import CommentType, UserType
from app.comments.models import Comment


@strawberry.type
class Query:
    """GraphQL queries для получения данных"""

    @strawberry.field
    def comments(
            self,
            limit: Optional[int] = None,
            offset: Optional[int] = None
    ) -> List[CommentType]:
        """
        Получить список комментариев верхнего уровня (без родителей)

        Args:
            limit: Максимальное количество комментариев (для пагинации)
            offset: Смещение для пагинации

        Returns:
            Список комментариев
        """
        queryset = (
            Comment.objects.filter(reply__isnull=True)
            .select_related('user')
            .prefetch_related('attachments', 'replies')
            .order_by('-created_at')
        )

        if offset:
            queryset = queryset[offset:]

        if limit:
            queryset = queryset[:limit]

        return list(queryset)

    @strawberry.field
    def comment(self, id: int) -> Optional[CommentType]:
        """
        Получить конкретный комментарий по ID

        Args:
            id: ID комментария

        Returns:
            Комментарий или None если не найден
        """
        try:
            return (
                Comment.objects
                .select_related('user')
                .prefetch_related('attachments', 'replies')
                .get(pk=id)
            )
        except Comment.DoesNotExist:
            return None

    @strawberry.field
    def comment_replies(self, comment_id: int) -> List[CommentType]:
        """
        Получить все ответы на конкретный комментарий

        Args:
            comment_id: ID родительского комментария

        Returns:
            Список ответов
        """
        return list(
            Comment.objects
            .filter(reply_id=comment_id)
            .select_related('user')
            .prefetch_related('attachments')
            .order_by('created_at')
        )

    @strawberry.field
    def my_comments(self, info) -> List[CommentType]:
        """
        Получить все комментарии текущего пользователя

        Args:
            info: GraphQL context (автоматически передается)

        Returns:
            Список комментариев пользователя

        Raises:
            GraphQLError: Чистая ошибка без traceback
        """
        user = info.context.request.user

        if not user.is_authenticated:
            raise GraphQLError(
                "Требуется авторизация!",
                extensions={"code": "UNAUTHORIZED"}
            )

        return list(
            Comment.objects
            .filter(user=user)
            .select_related('user')
            .prefetch_related('attachments', 'replies')
            .order_by('-created_at')
        )

    @strawberry.field
    def search_comments(self, query: str, limit: int = 50) -> List[CommentType]:
        """
        Поиск комментариев по тексту

        Args:
            query: Поисковый запрос
            limit: Максимальное количество результатов (по умолчанию 50)

        Returns:
            Список найденных комментариев
        """
        if not query or len(query) < 2:
            return []

        return list(
            Comment.objects
            .filter(text__icontains=query)
            .select_related('user')
            .prefetch_related('attachments')
            .order_by('-created_at')[:limit]
        )

    @strawberry.field
    def me(self, info) -> Optional[UserType]:
        """
        Получить информацию о текущем авторизованном пользователе

        Args:
            info: GraphQL context (автоматически передается)

        Returns:
            Текущий пользователь или None если не авторизован
        """
        user = info.context.request.user

        if user.is_authenticated:
            return user

        return None

    @strawberry.field
    def comment_count(self) -> int:
        """
        Получить общее количество комментариев в системе

        Returns:
            Количество комментариев
        """
        return Comment.objects.count()

    @strawberry.field
    def top_level_comment_count(self) -> int:
        """
        Получить количество комментариев верхнего уровня (без родителей)

        Returns:
            Количество корневых комментариев
        """
        return Comment.objects.filter(reply__isnull=True).count()

    @strawberry.field
    def user_comment_count(self, info) -> int:
        """
        Получить количество комментариев текущего пользователя

        Args:
            info: GraphQL context

        Returns:
            Количество комментариев пользователя

        Raises:
            GraphQLError: Чистая ошибка без traceback
        """
        user = info.context.request.user

        if not user.is_authenticated:
            raise GraphQLError(
                "Требуется авторизация!",
                extensions={"code": "UNAUTHORIZED"}
            )

        return Comment.objects.filter(user=user).count()


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)