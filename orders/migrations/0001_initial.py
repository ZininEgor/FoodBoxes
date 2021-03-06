# Generated by Django 3.1.7 on 2021-03-13 10:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('carts', '0003_auto_20210307_1236'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('delivery_at', models.DateTimeField(blank=True, null=True)),
                ('address', models.CharField(max_length=256)),
                ('status', models.CharField(choices=[('created', 'Создан'), ('delivered', 'Доставлен'), ('processed', 'В обработке'), ('cancelled', 'Отменен')], default='created', max_length=13)),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='carts.cart')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
