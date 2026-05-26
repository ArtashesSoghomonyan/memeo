import os

from django.contrib.auth import get_user_model
from django.db import models


def get_post_path(instance, filename):
    # Get the file extension (e.g., .jpg, .png)
    ext = filename.split('.')[-1]
    # Create a new name using the user's ID
    new_filename = f'{instance.author.id}_post_{instance.id}.{ext}'
    # Return the path: 'posts/1_post_8.jpg'
    return os.path.join('posts/', new_filename)


class Post(models.Model):
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='posts'
    )
    image = models.ImageField(upload_to=get_post_path, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    likes = models.ManyToManyField(
        get_user_model(), related_name='liked_posts', blank=True
    )
    publication_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username}-{self.description[:30]}'

    def number_of_likes(self):
        return self.likes.count()


class Comment(models.Model):
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='comments'
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(blank=False, null=False)
    publication_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} - {self.content[:30]}'
