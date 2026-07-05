from urllib.parse import quote
from django import template

register = template.Library()


@register.filter(name="encode_uri")
def encode_uri(value):
    """
    Safely percent-encode an Event Registry article URI (which can contain
    slashes and other reserved characters) so it can be used as a single
    path segment in a Django URL. Pair with `unquote()` on the receiving
    end in the view.

    Usage in template:
        {% url 'news_detail' article.uri|encode_uri %}
    """
    if value is None:
        return ""
    return quote(str(value), safe="")


@register.filter(name="get_item")
def get_item(dictionary, key):
    """Allows dict lookups with a variable key inside templates."""
    if not dictionary:
        return None
    return dictionary.get(key)


@register.filter(name="sentiment_label")
def sentiment_label(score):
    """Convert Event Registry's numeric sentiment (-1..1) into a word + css class."""
    if score is None:
        return None
    try:
        score = float(score)
    except (TypeError, ValueError):
        return None
    if score > 0.15:
        return "Positive"
    if score < -0.15:
        return "Negative"
    return "Neutral"