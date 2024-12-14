# Generated by Django 3.1.12 on 2024-12-13 07:52

import cart.models
from django.db import migrations, models # type: ignore
import djongo.models.fields # type: ignore


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=20)),
                ('addresses', djongo.models.fields.ArrayField(model_container=cart.models.Address)),
                ('payment_methods', djongo.models.fields.ArrayField(model_container=cart.models.PaymentMethod)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
