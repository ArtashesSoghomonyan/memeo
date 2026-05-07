from django.http import HttpResponseNotFound
from django.shortcuts import render

from posts.models import Post


def home(request):
    """View for the home page."""

    context = {
        'title': 'Homepage',
        'posts': Post.objects.all().order_by('-publication_date'),
    }

    return render(request, 'pages/home.html', context)


# Error pages


def status_404(request, exception):
    context = {
        'status_code': 404,
        'message': 'Page not found',
    }
    return render(request, 'error.html', context, status=404)
