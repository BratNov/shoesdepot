from .models import Category


def categories(request):
    context = Category.objects.all()
    return {'categories': context}
