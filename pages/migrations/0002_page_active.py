# Generated by Django 3.1.5 on 2021-07-12 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
