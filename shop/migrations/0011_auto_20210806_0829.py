# Generated by Django 3.1.5 on 2021-08-06 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20210804_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='short_description',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
    ]
