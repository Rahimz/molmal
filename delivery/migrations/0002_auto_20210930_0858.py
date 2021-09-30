# Generated by Django 3.1.5 on 2021-09-30 05:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_order_user'),
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverycontainer',
            name='admin_check',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='deliverycontainer',
            name='done',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='deliverycontainer',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.order'),
        ),
    ]
