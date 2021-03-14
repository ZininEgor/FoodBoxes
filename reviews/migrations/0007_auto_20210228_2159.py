# Generated by Django 3.1.7 on 2021-02-28 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_auto_20210228_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='status',
            field=models.CharField(
                choices=[
                    ('new',
                     'на модерации'),
                    ('published',
                     'опубликован'),
                    ('hidden',
                     'отклонен')],
                default='new',
                max_length=13),
        ),
    ]
