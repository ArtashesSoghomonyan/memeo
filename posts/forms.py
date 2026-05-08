from django import forms
from django.forms import ModelForm

from .models import Comment, Post


class PostForm(ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'border-2'}))

    class Meta:
        model = Post
        fields = ['image', 'description']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
