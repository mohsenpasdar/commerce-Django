# Generated by Django 4.1.6 on 2023-02-24 08:03

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_auctionlisting_current_bid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlisting',
            name='current_bid',
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='date_ended',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 3, 11, 33, 34, 565699)),
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('bidder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auctions.auctionlisting')),
            ],
        ),
    ]
