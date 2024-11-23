from django import forms
from i18nfield.forms import I18nModelForm

from .models import Settings


class SettingsForm(I18nModelForm):
    auth_token = forms.CharField(
        label="Token",
        max_length=100,
        widget=forms.PasswordInput,
        required=False,
    )

    def __init__(self, *args, event=None, **kwargs):
        self.instance, _ = Settings.objects.get_or_create(event=event)
        super().__init__(*args, **kwargs, instance=self.instance, locales=event.locales)

    def clean_auth_token(self):
        return self.cleaned_data["auth_token"] or self.instance.auth_token

    class Meta:
        model = Settings
        exclude = ("event",)
        # widgets = {}
