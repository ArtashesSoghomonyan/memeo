from django.shortcuts import render

from posts.models import Post


def home(request):
    """ View for the home page. """

    context = {
        'posts': Post.objects.all().order_by('-publication_date'),
    }

    return render(request, 'pages/home.html', context)
