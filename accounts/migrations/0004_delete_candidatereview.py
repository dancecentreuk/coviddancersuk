# Generated by Django 3.1.1 on 2020-10-27 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_candidatereview'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CandidateReview',
        ),
    ]