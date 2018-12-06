def get_unique_slug(instance, field_name_1, field_name_2):
    count = 0
    field_name_2 = field_name_2.strftime("%y-%b-%d")
    slug = "{slug1}-{slug2}".format(slug1=field_name_1, slug2=field_name_2)
    Klass = instance.__class__
    while Klass.objects.filter(slug=slug).exists():
        count = count + 1
        slug = "{slug1}-{slug2}-{slug3}".format(slug1=field_name_1, slug2=field_name_2, slug3=count)
    return slug
