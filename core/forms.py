from django import forms
from .utils import SUPPORTED_LANGUAGES, LANGUAGE_LABELS


class TranslationWidget(forms.MultiWidget):
    """
    Renders one input per language instead of raw JSON.

    Admin displays:
        EN:      [______________________________]
        简体中文: [______________________________]
        繁體中文: [______________________________]
    """

    def __init__(self, long_text=False, attrs=None):
        widget_cls = forms.Textarea if long_text else forms.TextInput
        widgets = []
        for lang in SUPPORTED_LANGUAGES:
            w = widget_cls(attrs={"placeholder": LANGUAGE_LABELS[lang]})
            if long_text:
                w.attrs.update({"rows": 3, "style": "width:100%"})
            else:
                w.attrs.update({"style": "width:100%"})
            widgets.append(w)
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, dict):
            return [value.get(lang, "") for lang in SUPPORTED_LANGUAGES]
        return [""] * len(SUPPORTED_LANGUAGES)

    def subwidgets(self, name, value, attrs=None):
        # Used by the template to render each sub-widget with its label
        decompressed = self.decompress(value)
        for index, widget in enumerate(self.widgets):
            lang = SUPPORTED_LANGUAGES[index]
            yield {
                "label": LANGUAGE_LABELS[lang],
                "widget": widget.render(f"{name}_{index}", decompressed[index], attrs),
            }


class TranslationFormField(forms.MultiValueField):
    """
    MultiValueField that compresses 3 language inputs into a single JSON dict.
    """

    def __init__(self, long_text=False, **kwargs):
        kwargs.setdefault("require_all_fields", False)
        kwargs.setdefault("required", False)
        fields = [forms.CharField(required=False, strip=True) for _ in SUPPORTED_LANGUAGES]
        widget = TranslationWidget(long_text=long_text)
        super().__init__(fields=fields, widget=widget, **kwargs)

    def compress(self, data_list):
        result = {}
        for i, lang in enumerate(SUPPORTED_LANGUAGES):
            result[lang] = data_list[i].strip() if i < len(data_list) and data_list[i] else ""
        return result