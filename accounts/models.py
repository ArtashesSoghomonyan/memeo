import os

from django.contrib.auth import get_user_model
from django.db import models


def get_profile_path(instance, filename):
    # Get the file extension (e.g., .jpg, .png)
    ext = filename.split('.')[-1]
    # Create a new name using the user's ID
    new_filename = f'{instance.user.id}_profile.{ext}'
    # Return the path: 'profile_pics/1_profile.jpg'
    return os.path.join('profile_pics', new_filename)


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to=get_profile_path, default='default.jpg', blank=True)
    bio = models.CharField(max_length=500, blank=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username
