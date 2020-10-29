from django.db import models
from accounts.models import User, Candidate


# Create your models here.


class CandidateReview(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)
    rating = models.FloatField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    is_allowed = models.BooleanField(default=True)

    def __str__(self):
        return self.author.username

