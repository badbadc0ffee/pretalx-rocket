import logging
import re

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from pretalx.common.language import language
from pretalx.orga.signals import nav_event_settings
from pretalx.submission.models import Submission
from rocketchat_API.rocketchat import RocketChat

logger = logging.getLogger(__name__)


@receiver(nav_event_settings)
def rocket_settings(sender, request, **kwargs):
    if not request.user.has_perm("orga.change_settings", request.event):
        return []
    return [
        {
            "label": "Rocket.Chat",
            "url": reverse(
                "plugins:pretalx_rocket:settings",
                kwargs={"event": request.event.slug},
            ),
            "active": request.resolver_match.url_name
            == "plugins:pretalx_rocket:settings",
        }
    ]


def quote(text):
    if text == "":
        return "nothing"
    lines = text.split("\n")
    lines = [line for line in lines if line.strip()]
    if len(text) > 50 or len(lines) > 1:
        for line in lines:
            line = "> " + line
        quote = "\n".join(lines)
    else:
        quote = "`" + " ".join(lines) + "`"
    return quote


@receiver(pre_save, sender=Submission)
def pre_save_handler(sender, instance, **kwargs):
    if "pretalx_rocket" not in instance.event.plugin_list:
        return None
    try:
        rocket_settings = getattr(instance.event, "rocket_settings", None)
        with language("en"):
            changed = False
            if instance.pk and rocket_settings.post_modified_sessions:
                message = f"Submission <{instance.orga_urls.base.full()}|{instance.code}> was updated:"
                existing = sender.objects.get(pk=instance.pk)
                for field in sender._meta.fields:
                    field_name = field.name
                    if field_name in re.split(r"[ ,]+", rocket_settings.exclude_fields):
                        continue
                    old_value = getattr(existing, field_name)
                    new_value = getattr(instance, field_name)
                    field_name = Submission._meta.get_field(field_name).verbose_name
                    if old_value != new_value:
                        changed = True
                        if new_value is True:
                            message += f"\n- [x] {field_name} changed from {quote(old_value)} to {quote(new_value)}"
                        elif new_value is False:
                            message += f"\n- [ ] {field_name} changed from {quote(old_value)} to {quote(new_value)}"
                        else:
                            message += f"\n{field_name} changed from {quote(old_value)} to {quote(new_value)}"
            else:
                if rocket_settings.post_new_sessions:
                    changed = True
                    message = f"New submission <{instance.orga_urls.base.full()}|{instance.code}>."
            if changed:
                rocket = RocketChat(
                    user_id=rocket_settings.user_id,
                    auth_token=rocket_settings.auth_token,
                    server_url=rocket_settings.server_url,
                )
                rocket.chat_post_message(
                    message,
                    channel=rocket_settings.channel,
                )
    except Exception:
        return None
