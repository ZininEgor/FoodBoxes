# Generated by Django 3.1.7 on 2021-03-13 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20210313_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]