from django.contrib import admin
from .models import Venue, VenueReview

# Register your models here.


admin.site.register(Venue),
admin.site.register(VenueReview),