# Generated by Django 3.2 on 2021-05-03 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzaapp', '0006_alter_ordermodel_ordereditems'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='address',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='phone',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='username',
            field=models.CharField(max_length=10),
        ),
    ]
