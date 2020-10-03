from django.db import models
from django.utils import timezone


class Posts(models.Model):
    boast = models.BooleanField(default=True)
    text = models.CharField(max_length=140)
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    post_date = models.DateTimeField(default=timezone.now)

    @property
    def score(self):
        return self.up_votes - self.down_votes
