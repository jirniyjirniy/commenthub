from django.contrib import admin

from app.comments.models import Comment, CommentAttachment


admin.site.register(Comment)
admin.site.register(CommentAttachment)
