# Generated by Django 4.1.7 on 2023-07-29 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Carts',
            new_name='Cart',
        ),
    ]
