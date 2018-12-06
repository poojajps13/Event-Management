def registration_unique_slug(instance, new_slug):
    count = 1
    slug = "{slug}_{count}".format(slug=new_slug, count=count)
    Klass = instance.__class__
    while Klass.objects.filter(registration_id=slug).exists():
        count = count + 1
        slug = "{slug}_{count}".format(slug=new_slug, count=count)
    return slug


def transaction_unique_slug(instance, new_slug):
    count = 1
    slug = "{slug}-{count}".format(slug=new_slug, count=count)
    Klass = instance.__class__
    while Klass.objects.filter(transaction_id=slug).exists():
        count = count + 1
        slug = "{slug}-{count}".format(slug=new_slug, count=count)
    return slug
