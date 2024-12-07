from .models import Tag

def products_tags_processor(request):
    """
    Adds categories to the context for all templates.
    """
    tags = Tag.objects.all()
    return {"tags": tags}