from django.urls import path
from .views import (
    CommentListCreateAPIView,
    CommentDetailAPIView,
    CommentPreviewAPIView,
    comment_text_preview,
    health_check
)

urlpatterns = [
    path("", CommentListCreateAPIView.as_view(), name="comment-list-create"),

    path("<int:pk>/", CommentDetailAPIView.as_view(), name="comment-detail"),
    path("preview/", CommentPreviewAPIView.as_view(), name="comment-preview"),
    path("preview-text/", comment_text_preview, name="comment-text-preview"),
    path("health/", health_check, name="health-check"),
]