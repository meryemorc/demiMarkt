# Generated by Django 3.1.12 on 2024-12-14 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$260000$unique_salt$hashed_password_value', max_length=128),
            preserve_default=False,
        ),
    ]
