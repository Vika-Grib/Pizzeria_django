# Generated by Django 4.2.1 on 2023-11-10 17:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pizzeria_back', '0002_product_pizza_delete_project'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Product_pizza',
        ),
    ]