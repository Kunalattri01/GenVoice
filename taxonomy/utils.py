from django.utils.text import slugify


def generate_unique_slug(model_class, value, instance_pk=None, slug_field="slug"):
    """
    Generates a unique slug for any model.
    Appends -2, -3, ... if a slug already exists.
    Excludes the current instance when editing.
    """

    base_slug = slugify(value)[:170] or "item"
    slug = base_slug
    counter = 2

    qs = model_class.objects.all()

    if instance_pk:
        qs = qs.exclude(pk=instance_pk)

    while qs.filter(**{slug_field: slug}).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug