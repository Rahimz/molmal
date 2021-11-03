# Generated by Django 3.1.5 on 2021-11-03 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0005_deliverycontainer_fa_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverycontainer',
            name='fa_time',
            field=models.CharField(choices=[('morning', '9-12'), ('afternoon', '13-16')], default='morning', max_length=200),
        ),
    ]
