# Generated by Django 3.1 on 2020-08-25 03:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_watchlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='user',
            new_name='seller',
        ),
        migrations.AddField(
            model_name='listing',
            name='users_watching',
            field=models.ManyToManyField(blank=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='WatchList',
        ),
    ]