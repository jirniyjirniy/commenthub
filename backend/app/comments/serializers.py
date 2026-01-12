import io
import os
from typing import List, Dict, Any

import requests
from PIL import Image
from django.core.files.base import ContentFile
from django.conf import settings
import bleach
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
import cloudinary.uploader

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from app.comments.models import Comment, CommentAttachment
from app.comments.tasks import send_reply_notification_email
from app.users.serializers import UserSerializer


class CommentPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "text", "created_at"]


class CommentTextPreviewSerializer(serializers.Serializer):
    text = serializers.CharField(required=True)

    ALLOWED_TAGS = ["a", "code", "i", "strong", "p", "br", "em", "b"]
    ALLOWED_ATTRIBUTES = {"a": ["href", "title"]}

    def validate_text(self, value):
        cleaned_text = bleach.clean(
            value,
            tags=self.ALLOWED_TAGS,
            attributes=self.ALLOWED_ATTRIBUTES,
            strip=True,
        )

        cleaned_text = bleach.linkify(
            cleaned_text,
            parse_email=False,
            callbacks=[],
        )

        return cleaned_text


class CommentTextPreviewResponseSerializer(serializers.Serializer):
    """Response for text preview endpoint"""
    text = serializers.CharField()


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    attachments = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            "text",
            "created_at",
            "updated_at",
            "reply",
            "replies",
            "attachments",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "user", "attachments"]

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "file": {"type": "string"},
                    "media_type": {"type": "string"},
                }
            }
        }
    )
    def get_attachments(self, obj) -> List[Dict[str, Any]]:
        return [
            {"id": a.id, "file": a.file, "media_type": a.media_type}
            for a in obj.attachments.all()
        ]

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "user": {"type": "object"},
                    "text": {"type": "string"},
                    "created_at": {"type": "string", "format": "date-time"},
                    "updated_at": {"type": "string", "format": "date-time"},
                    "reply": {"type": "integer", "nullable": True},
                    "replies": {"type": "array"},
                    "attachments": {"type": "array"},
                }
            }
        }
    )
    def get_replies(self, obj) -> List[Dict[str, Any]]:
        """Get all replies to this comment"""
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []


class CommentCreateSerializer(serializers.ModelSerializer):
    ALLOWED_TAGS = ["a", "code", "i", "strong", "p", "br", "em", "b"]
    ALLOWED_ATTRIBUTES = {"a": ["href", "title"]}

    user = UserSerializer(read_only=True)
    files = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )
    recaptcha_token = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "text",
            "reply",
            "user",
            "created_at",
            "updated_at",
            "files",
            "recaptcha_token",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "user"]

    def validate_text(self, value):
        cleaned_text = bleach.clean(
            value,
            tags=self.ALLOWED_TAGS,
            attributes=self.ALLOWED_ATTRIBUTES,
            strip=True,
        )

        cleaned_text = bleach.linkify(
            cleaned_text,
            parse_email=False,
            callbacks=[],
        )

        return cleaned_text

    def validate_recaptcha_token(self, value):
        """Validate reCAPTCHA token with Google's API"""
        if not settings.RECAPTCHA_PRIVATE_KEY:
            raise serializers.ValidationError(
                "reCAPTCHA is not configured on the server"
            )

        response = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                "secret": settings.RECAPTCHA_PRIVATE_KEY,
                "response": value,
            },
            timeout=10,
        )

        result = response.json()

        if not result.get("success", False):
            error_codes = result.get("error-codes", [])
            if "timeout-or-duplicate" in error_codes:
                raise serializers.ValidationError(
                    "CAPTCHA has expired. Please try again."
                )
            raise serializers.ValidationError("Invalid CAPTCHA. Please try again.")

        return value

    def validate_files(self, files):
        for i, file in enumerate(files):
            ext = os.path.splitext(file.name)[1].lower()
            if ext == ".txt":
                if file.size > 100 * 1024:
                    raise serializers.ValidationError(
                        f"File {file.name} is too big. Max TXT file size is 100KB."
                    )
                continue
            elif ext in [".jpg", ".jpeg", ".png", ".gif"]:
                if file.size > 5 * 1024 * 1024:
                    raise serializers.ValidationError(
                        f"File {file.name} is too big. Max JPG, PNG, GIF file size is 5MB."
                    )
                file = self._process_image(file, ext)
                files[i] = file
            else:
                raise serializers.ValidationError(
                    f"File {file.name} has invalid format. Only TXT, JPG, PNG, GIF allowed."
                )

        return files

    def _process_image(self, file, ext):
        try:
            image = Image.open(file)

            if image.width > 320 or image.height > 240:
                image.thumbnail((320, 240))

                output = io.BytesIO()
                img_format = (
                    image.format if image.format else ext.replace(".", "").upper()
                )
                if img_format == "JPG":
                    img_format = "JPEG"

                image.save(output, format=img_format)
                output.seek(0)

                return ContentFile(output.read(), name=file.name)

            return file
        except Exception:
            raise serializers.ValidationError(f"Invalid image file: {file.name}")

    def create(self, validated_data):
        attachments_data = validated_data.pop("files", [])
        validated_data.pop("recaptcha_token", None)
        user = self.context["request"].user
        validated_data["user"] = user

        comment = super().create(validated_data)

        for idx, file in enumerate(attachments_data):
            ext = os.path.splitext(file.name)[1].lower()
            media_type = "image" if ext in [".jpg", ".jpeg", ".png", ".gif"] else "file"

            try:
                cloudinary_file = cloudinary.uploader.upload(
                    file,
                    resource_type="auto",
                )
                file_url = cloudinary_file["secure_url"]
            except cloudinary.exceptions.Error:
                raise serializers.ValidationError("Failed to upload file to Cloudinary")

            CommentAttachment.objects.create(
                comment=comment, file=file_url, media_type=media_type
            )

        if comment.reply:
            self._send_reply_notification(comment, user)

        return comment

    def to_representation(self, instance):
        """
        Используем CommentSerializer для возврата полного объекта с attachments
        """
        return CommentSerializer(instance, context=self.context).data

    def _send_reply_notification(self, comment, user):
        root_comment = comment.get_root_comment()
        channel_layer = get_channel_layer()
        serialized_reply = CommentSerializer(comment).data

        group_name = f"comment_{root_comment.id}"
        async_to_sync(channel_layer.group_send)(
            group_name, {"type": "new_reply", "reply": serialized_reply}
        )

        if user != root_comment.user:
            send_reply_notification_email.delay(
                user_email=root_comment.user.email,
                comment_text_short=serialized_reply["text"][:200],
            )