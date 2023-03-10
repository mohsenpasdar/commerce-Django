# Generated by Django 4.1.6 on 2023-03-07 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auctionlisting_watchlist_delete_watchlistitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='category',
            field=models.CharField(choices=[('BEAUTY', 'Beauty & Personal Care'), ('BOOKS', 'Books'), ('ELECTRONICS', 'Electronics'), ('FASHION', 'Fashion'), ('FOOD', 'Food & Beverage'), ('HEALTH', 'Health & Wellness'), ('HOME', 'Home'), ('JEWELRY', 'Jewelry & Accessories'), ('MUSIC', 'Music & Entertainment'), ('OFFICE', 'Office & Stationery'), ('PETS', 'Pet Supplies'), ('SPORTS', 'Sports'), ('TOYS', 'Toys'), ('TRAVEL', 'Travel & Leisure'), ('VEHICLES', 'Vehicles & Automotive'), ('OTHER', 'Other')], default='OTHER', max_length=20),
        ),
    ]
