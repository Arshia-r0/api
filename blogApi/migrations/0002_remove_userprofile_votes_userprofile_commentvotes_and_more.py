# Generated by Django 5.0.4 on 2024-04-18 14:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogApi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='Votes',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='commentVotes',
            field=models.ManyToManyField(related_name='commentVotes', through='blogApi.Votes', to='blogApi.comment'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='postVotes',
            field=models.ManyToManyField(related_name='postVotes', through='blogApi.Votes', to='blogApi.post'),
        ),
        migrations.AddField(
            model_name='votes',
            name='comment',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='blogApi.comment'),
        ),
        migrations.AlterField(
            model_name='votes',
            name='post',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='blogApi.post'),
        ),
    ]
