# Generated by Django 3.1 on 2020-08-24 14:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_remove_listing_winner'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='winner',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='winnings', to=settings.AUTH_USER_MODEL),
        ),
    ]
