# Generated by Django 5.0.3 on 2024-03-25 17:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_comments_author_comments_comment_text_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bids',
            name='bid',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='bids',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_bid', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listings',
            name='price',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bid_price', to='auctions.bids'),
        ),
    ]
