# Generated by Django 4.1.3 on 2023-01-25 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_rename_category_category_categoryname'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='isActive',
            field=models.BooleanField(default=1),
        ),
    ]