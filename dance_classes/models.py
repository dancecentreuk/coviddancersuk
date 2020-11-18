from django.db import models
from accounts.models import User, Candidate
from pages.choices import location_choices, dance_styles, day, level, age_choices
from django.template.defaultfilters import slugify
from django.urls import reverse


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
    dance_class_image_1 =models.ImageField(upload_to='dance-class-image/%Y/%m/%d', blank=True)
    dance_class_image_2 =models.ImageField(upload_to='dance-class-image/%Y/%m/%d', blank=True)
    dance_class_image_3 =models.ImageField(upload_to='dance-class-image/%Y/%m/%d', blank=True)
    faq = models.TextField(blank=True, null=True)
    clothes = models.CharField(max_length=250, blank=True)
    experience = models.CharField(max_length=250, blank=True)
    average_age = models.CharField(max_length=250, blank=True)
    drop_in = models.CharField(max_length=250, blank=True)
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
        return f'{self.id}-{self.dance_style_choice} by {self.author.user}'

    # def get_absolute_url(self):
    #     return reverse('dance-class-detail', kwargs={'id': self.id})



class ClassImage(models.Model):
    title = models.CharField(max_length=180)
    profile_image = models.ImageField(upload_to='dance-class-pictures/%Y/%m/%d')
    owner = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250)
    dance_class = models.ForeignKey(WeeklyDanceClass, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.id} - photo for {self.dance_class.id}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class DanceClassReview(models.Model):
    danceClass = models.ForeignKey(WeeklyDanceClass, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)
    rating = models.FloatField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    is_allowed = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.id}-{self.danceClass} by {self.author.username}'





