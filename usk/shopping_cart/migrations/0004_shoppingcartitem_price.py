# Generated by Django 4.2 on 2023-04-24 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_cart', '0003_shoppingcart_closed'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcartitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
    ]
