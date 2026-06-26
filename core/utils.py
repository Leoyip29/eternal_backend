SUPPORTED_LANGUAGES = ["en", "zh_hans", "zh_hant"]
DEFAULT_LANGUAGE = "en"

LANGUAGE_LABELS = {
    "en": "English",
    "zh_hans": "Simplified Chinese (简体中文)",
    "zh_hant": "Traditional Chinese (繁體中文)",
}

ACCEPT_LANGUAGE_MAP = {
    "en": "en",
    "zh-hans": "zh_hans",
    "zh-cn": "zh_hans",
    "zh-sg": "zh_hans",
    "zh-my": "zh_hans",
    "zh-hant": "zh_hant",
    "zh-tw": "zh_hant",
    "zh-hk": "zh_hant",
    "zh-mo": "zh_hant",
    "zh": "zh_hant",  # generic Chinese defaults to Traditional
}


def default_translation():
    return {"en": "", "zh_hans": "", "zh_hant": ""}


def get_language_from_request(request):
    """
    Resolve active language from:
      1. ?lang=  query param  (highest priority — explicit frontend choice)
      2. Accept-Language header
      3. Default: English
    """
    # 1. Query param
    lang = None
    if hasattr(request, "query_params"):
        lang = request.query_params.get("lang")
    elif hasattr(request, "GET"):
        lang = request.GET.get("lang")

    if lang in SUPPORTED_LANGUAGES:
        return lang

    # 2. Accept-Language header
    accept = request.META.get("HTTP_ACCEPT_LANGUAGE", "")
    for part in accept.lower().split(","):
        code = part.strip().split(";")[0].strip()
        if code in ACCEPT_LANGUAGE_MAP:
            return ACCEPT_LANGUAGE_MAP[code]

    return DEFAULT_LANGUAGE


def resolve_translation(value, lang=None):
    """Return the translated string for a given language, falling back to English."""
    if not isinstance(value, dict):
        return value or ""
    lang = lang or DEFAULT_LANGUAGE
    return value.get(lang) or value.get(DEFAULT_LANGUAGE) or ""