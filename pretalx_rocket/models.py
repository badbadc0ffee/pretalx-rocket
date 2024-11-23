from django.db import models


class Settings(models.Model):
    event = models.OneToOneField(
        to="event.Event",
        on_delete=models.CASCADE,
        related_name="rocket_settings",
    )
    user_id = models.CharField(
        verbose_name="User ID",
        max_length=100,
    )
    auth_token = models.CharField(
        verbose_name="Token",
        max_length=100,
    )
    server_url = models.URLField(
        verbose_name="Server URL",
        default="https://demo.rocket.chat",
    )
    channel = models.CharField(max_length=100)
    post_new_sessions = models.BooleanField(
        verbose_name="Post new sessions.",
        default=False,
    )
    post_modified_sessions = models.BooleanField(
        verbose_name="Post modified sessions.",
        default=True,
    )
    exclude_fields = models.CharField(
        max_length=100,
        verbose_name="Exclude",
        default="internal_notes,access_code,review_code,invitation_token",
    )
