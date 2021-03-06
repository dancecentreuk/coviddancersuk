from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from pages.choices import (gender_choices, location_choices, height_in, height_ft, weight_lb, weight_st,
                           waist, bust, hip, shoe_size, eye_color, hair_color, build, primary_job)
from PIL import Image
from django.core.files.storage import default_storage
from io import BytesIO

class User(AbstractUser):
    is_candidate = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    mobile = models.CharField(max_length=20)
    gender = models.CharField(
        choices=gender_choices,
        max_length=1,
        default=None,
    )
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profiles/%Y/%m/%d', default='candidate.png')
    candidate_location = models.CharField(
        choices=location_choices,
        max_length=20,
    )
    experience = models.TextField(blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    height_ft = models.CharField(
        choices=height_ft,
        max_length=2,
        default=None,
        null=True,
        blank=True,
    )
    height_in = models.CharField(
        choices=height_in,
        max_length=2,
        default=None,
        null=True,
        blank=True,
    )
    weight_st = models.CharField(
        choices=weight_st,
        max_length=2,
        default=None,
        null=True,
        blank=True,
    )
    weight_lb = models.CharField(
        choices=weight_lb,
        max_length=2,
        default=None,
        null=True,
        blank=True,
    )
    waist_size = models.CharField(
        choices=waist,
        max_length=2,
        default=None,
        null=True,
        blank=True,
    )

    bust = models.CharField(
        choices=bust,
        max_length=2,
        default=None,
        null=True,
        blank=True,
    )

    hip = models.CharField(
        choices=hip,
        max_length=2,
        default=None,
        null=True,
        blank=True,
    )

    shoe_size = models.CharField(
        choices=shoe_size,
        max_length=2,
        default=None,
        null=True,
        blank=True,
    )

    eye_color = models.CharField(
        choices=eye_color,
        max_length=10,
        default=None,
        null=True,
        blank=True,
    )

    hair_color = models.CharField(
        choices=hair_color,
        max_length=200,
        default=None,
        null=True,
        blank=True,
    )

    build = models.CharField(
        choices=build,
        max_length=20,
        default=None,
        null=True,
        blank=True,
    )

    primary_job = models.CharField(
        choices=primary_job,
        max_length=20,
        default=None,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        memfile = BytesIO()


        img = Image.open(self.profile_image)
        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size, Image.ANTIALIAS)
            img.save(memfile, 'PNG', quality=95)
            default_storage.save(self.profile_image.name, memfile)
            memfile.close()
            img.close()





class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20)
    profile_image = models.ImageField(upload_to='profiles/%Y/%m/%d', default='employer.png')
    company_info = models.TextField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    is_company = models.BooleanField(default=False)
    company_email = models.CharField(max_length=200, blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        memfile = BytesIO()



        img = Image.open(self.profile_image)
        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size, Image.ANTIALIAS)
            img.save(memfile, 'PNG', quality=95)
            default_storage.save(self.profile_image.name, memfile)
            memfile.close()
            img.close()





class CandidateImage(models.Model):
    title = models.CharField(max_length=180)
    profile_image = models.ImageField(upload_to='candidates-profiles/%Y/%m/%d')
    owner = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250)


    def __str__(self):
        return self.owner.user.username




    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     return super().save(*args, **kwargs)



    def save(self, *args, **kwargs):
        super().save()

        if not self.slug:
            self.slug = slugify(self.title)

        img = Image.open(self.profile_image.path)

        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.profile_image.path)

        return super().save(*args, **kwargs)






