# Generated by Django 5.0.4 on 2024-04-22 07:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogApi', '0004_alter_userprofile_followers'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='followers',
            field=models.ManyToManyField(blank=True, default=None, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
    ]
