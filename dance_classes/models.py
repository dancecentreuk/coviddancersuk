from django.db import models
from accounts.models import User, Candidate
from pages.choices import location_choices, dance_styles, day, level, age_choices

# Create your models here.


class WeeklyDanceClass(models.Model):
    author = models.ForeignKey(Candidate, models.CASCADE)
    dance_style_choice = models.CharField(
        choices=dance_styles,
        max_length=50
    )
    location = models.CharField(
        choices=location_choices,
        max_length=20,
    )
    day = models.CharField(
        choices = day,
        max_length=15,
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    price = models.FloatField()
    level = models.CharField(
        choices=level,
        max_length=45,
    )
    dance_class_image=models.ImageField(upload_to='dance-class-image/%Y/%m/%d', default='dance_class.jpg')
    faq = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=250)
    postcode = models.CharField(max_length=10)
    age_group = models.CharField(
        choices=age_choices,
        max_length=20,
    )
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    teacher = models.CharField(max_length=90, blank=True, null=True)
    about_dance_class = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    is_allowed = models.BooleanField(default=True)

    def __str__(self):
        return self.author.user.username
