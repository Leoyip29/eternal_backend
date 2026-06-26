from rest_framework import serializers
from .utils import get_language_from_request, DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES, resolve_translation


class TranslatedCharField(serializers.Field):
    """
    DRF field for TranslatedField.

    - In responses: returns the string for the active language only.
    - Accepts ?lang=zh_hans or Accept-Language header.
    - In write requests: accepts either a full dict or a plain string (stored as EN value).
    """

    def to_representation(self, value):
        request = self.context.get("request")
        lang = get_language_from_request(request) if request else DEFAULT_LANGUAGE
        return resolve_translation(value, lang)

    def to_internal_value(self, data):
        if isinstance(data, dict):
            unknown = [k for k in data if k not in SUPPORTED_LANGUAGES]
            if unknown:
                raise serializers.ValidationError(f"Unknown language keys: {unknown}")
            return data
        if isinstance(data, str):
            # convenience: plain string is stored as English value
            return {lang: (data if lang == DEFAULT_LANGUAGE else "") for lang in SUPPORTED_LANGUAGES}
        raise serializers.ValidationError("Expected a JSON object with language keys or a plain string.")


class TranslatedAllLanguagesField(serializers.Field):
    """
    Returns the full translation dict — useful for admin/editor API endpoints.
    """

    def to_representation(self, value):
        if isinstance(value, dict):
            return value
        return {lang: (value or "") for lang in SUPPORTED_LANGUAGES}

    def to_internal_value(self, data):
        if not isinstance(data, dict):
            raise serializers.ValidationError("Expected a JSON object with language keys.")
        unknown = [k for k in data if k not in SUPPORTED_LANGUAGES]
        if unknown:
            raise serializers.ValidationError(f"Unknown language keys: {unknown}")
        return data