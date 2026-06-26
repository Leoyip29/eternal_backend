from django.db import models
from django.core.exceptions import ValidationError
from .utils import SUPPORTED_LANGUAGES, default_translation


class TranslatedField(models.JSONField):
    """
    JSONField that enforces the shape:
        {"en": "...", "zh_hans": "...", "zh_hant": "..."}

    Pass long_text=True for fields that need a Textarea in the admin
    (e.g. body_text, description, answer).
    """

    def __init__(self, *args, long_text=False, **kwargs):
        self.long_text = long_text
        kwargs.setdefault("default", default_translation)
        super().__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        if not isinstance(value, dict):
            raise ValidationError("Translation must be a JSON object.")
        unknown = [k for k in value if k not in SUPPORTED_LANGUAGES]
        if unknown:
            raise ValidationError(f"Unknown language key(s): {unknown}. Allowed: {SUPPORTED_LANGUAGES}")
        for lang in SUPPORTED_LANGUAGES:
            if lang not in value:
                raise ValidationError(f"Missing translation for language: '{lang}'.")
            if not isinstance(value[lang], str):
                raise ValidationError(f"Value for '{lang}' must be a string.")

    def formfield(self, **kwargs):
        from .forms import TranslationFormField
        field = TranslationFormField(long_text=self.long_text)
        field.label = kwargs.get("label", "")
        return field

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.long_text:
            kwargs["long_text"] = self.long_text
        # remove default from kwargs since it's always set in __init__
        kwargs.pop("default", None)
        return name, path, args, kwargs