# Generated by Django 3.2.3 on 2021-05-28 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzaapp', '0014_pizzamodel_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pizzamodel',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='pizzamodel',
            name='price',
            field=models.CharField(max_length=100),
        ),
    ]
