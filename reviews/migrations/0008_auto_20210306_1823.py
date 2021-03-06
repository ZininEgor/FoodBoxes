# Generated by Django 3.1.7 on 2021-03-06 18:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0007_auto_20210228_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='author',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='my_reviews',
                to=settings.AUTH_USER_MODEL),
        ),
    ]
