# Generated by Django 4.1.7 on 2023-08-06 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_variation'),
        ('carts', '0002_rename_carts_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variation',
            field=models.ManyToManyField(blank=True, to='store.variation'),
        ),
    ]