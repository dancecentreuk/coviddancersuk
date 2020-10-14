from django.db import models
from accounts.models import Employer, User
from django.utils import timezone
from pages.choices import location_choices
from django.template.defaultfilters import slugify



class Advert(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    start_time = models.CharField(null=True, blank=True, max_length=9)
    finish_time = models.CharField(null=True, blank=True, max_length=9)
    is_posting = models.BooleanField(default=False)
    publish = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    fee = models.CharField(max_length=100)
    location = models.CharField(
        choices=location_choices,
        max_length=20,
    )
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Posting(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    body = models.TextField()
    author = models.ForeignKey(Employer, on_delete=models.CASCADE)
    cover_date = models.DateField(null=True)
    publish = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    fee = models.CharField(max_length=100)
    location = models.CharField(
        choices=location_choices,
        max_length=20,
    )
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

