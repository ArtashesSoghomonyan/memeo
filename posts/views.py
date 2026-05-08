from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Comment, Post


@login_required
def create_post(request):
    """View for creating a new post."""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'You have successfully created a post!')
            # TODO: change redirect
            # return redirect('post_detail', pk=post.id)
            return redirect('home')
    else:
        form = PostForm()

    context = {
        'title': 'Create Post',
        'form': form,
    }

    return render(request, 'posts/create_post.html', context)


def post_detail(request, pk):
    """View for displaying a single post."""
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('-publication_date')
    comment_form = CommentForm()
    like_count = post.likes.count()
    is_liked = (
        request.user.is_authenticated and post.likes.filter(id=request.user.id).exists()
    )
    context = {
        'title': f'{post.description[:30]}',
        'post': post,
        'like_count': like_count,
        'is_liked': is_liked,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_edit(request, pk):
    """View for editing a post."""
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        messages.error(request, 'You are not authorized to edit this post.')
        return redirect('post_detail', pk=post.id)  # type: ignore

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully edited the post!')
            return redirect('post_detail', pk=post.id)  # type: ignore
    else:
        form = PostForm(instance=post)

    context = {
        'title': f'Edit Post - {post.description[:30]}',
        'form': form,
        'post': post,
    }
    return render(request, 'posts/post_edit.html', context)


@login_required
def post_delete(request, pk):
    """View for deleting a post."""
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        messages.error(request, 'You are not authorized to delete this post.')
        return redirect('post_detail', pk=post.id)  # type: ignore

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'You have successfully deleted the post!')
        return redirect('home')
    else:
        context = {
            'title': f'Delete Post - {post.description[:30]}',
            'post': post,
        }
        return render(request, 'posts/post_delete.html', context)


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
    return redirect('post_detail', pk=pk)


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'You have successfully added a comment!')
    return redirect('post_detail', pk=post.pk)
