# Generated by Django 3.1 on 2020-08-26 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0024_listing_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='basePrice',
            field=models.DecimalField(decimal_places=0, max_digits=7),
        ),
    ]