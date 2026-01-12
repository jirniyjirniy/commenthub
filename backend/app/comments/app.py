from django.apps import AppConfig

class CommentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app.comments"
    verbose_name = "Comments"

    def ready(self):
        import app.comments.signals  # noqa: F401