# Generated by Django 2.2.12 on 2020-04-10 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bolaoapp', '0003_auto_20200409_2108'),
    ]

    operations = [
        migrations.AddField(
            model_name='partida',
            name='campeonato',
            field=models.CharField(default='campeonato', max_length=25),
            preserve_default=False,
        ),
    ]