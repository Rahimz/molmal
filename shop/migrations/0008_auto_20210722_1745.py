# Generated by Django 3.1.5 on 2021-07-22 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20210722_0535'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-created',)},
        ),
    ]
