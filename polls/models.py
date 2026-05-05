import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class Question(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text

    def was_published_recently(self) -> bool:
        return self.pub_date >= timezone.now() - datetime.timedelta(days=2)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.ManyToManyField(get_user_model(), related_name='votes', blank=True)

    def __str__(self):
        return f"{self.choice_text} - {self.question} ({self.votes})"

    def user_has_voted(self, user):
        return self.votes.filter(pk=user.id).exists()
