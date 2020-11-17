from django.db import models
from accounts.models import User
from pages.choices import location_choices
from django.template.defaultfilters import slugify



class Venue(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    venue_name = models.CharField(max_length=200, )
    slug = models.SlugField(max_length=250)
    address = models.CharField(max_length=250)
    location = models.CharField(
        choices=location_choices,
        max_length=20,
    )
    size_width_ft = models.IntegerField(blank=True, null=True)
    size_length_ft = models.IntegerField(blank=True, null=True)
    price = models.FloatField()
    mirrors = models.BooleanField(default=False)
    music_system = models.BooleanField(default=False)
    contact_person = models.CharField(max_length=100, )
    contact_number = models.CharField(max_length=13, blank=True)
    contact_email = models.CharField(max_length=250, blank=True)
    flooring = models.CharField(max_length=100, blank=True)
    about = models.TextField(blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    is_allowed = models.BooleanField(default=True)
    venue_image = models.ImageField(upload_to='venue-image/%Y/%m/%d', default='default_venue.jpg')
    venue_image_1 = models.ImageField(upload_to='venue-image/%Y/%m/%d', blank=True)
    venue_image_2 = models.ImageField(upload_to='venue-image/%Y/%m/%d', blank=True)
    venue_image_3 = models.ImageField(upload_to='venue-image/%Y/%m/%d', blank=True)
    faq = models.TextField(blank=True, null=True)

    postcode = models.CharField(max_length=10)


    def __str__(self):
        return f'{self.id}-{self.venue_name} by {self.author.username}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.venue_name)
        return super().save(*args, **kwargs)


class VenueReview(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)
    rating = models.FloatField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    is_allowed = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.id}-{self.venue} by {self.author.username}'


