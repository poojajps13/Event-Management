from django.utils.text import slugify
import string

def get_unique_slug(instance, slugable_field_name_1, slugable_field_name_2, slugable_field_name_3, new_slug=None):
    """
    Takes a model instance, sluggable field name (such as 'title') of that
    model as string, slug field name (such as 'slug') of the model as string;
    returns a unique slug as string.
    """
    count = 1
    if new_slug is None:
        slug = "{slug1}-{slug2}-{slug3}-{slug4}".format(
            slug1=slugable_field_name_1,
            slug2=slugable_field_name_2,
            slug3=slugable_field_name_3,
            slug4=count
        )
    new_slug = slug

    Klass = instance.__class__
    while (Klass.objects.filter(slug=new_slug).exists()):
        count = count + 1
        new_slug = "{slug}-{count}".format(
            slug=slug,
            count=count
        )
        return get_unique_slug(instance, slugable_field_name_1=slugable_field_name_1,
                               slugable_field_name_2=slugable_field_name_2, slugable_field_name_3=slugable_field_name_3,
                               new_slug=new_slug)
    return slug


def unique_slug(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    count = 1
    if new_slug is not None:
        slug = "{slug}-{randstr}".format(
            slug=new_slug,
            randstr=count
        )
    else:
        slug = slugify("Default")
    while True:
        print(slug)
        Klass = instance.__class__
        qs_exists = Klass.objects.filter(payment_id=slug).exists()
        if qs_exists:
            count = count + 1
            slug = "{slug}-{randstr}".format(
                slug=new_slug,
                randstr=count
            )
        else:
            break
    return slug