# Generated by Django 4.1.3 on 2022-12-27 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_auction_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amnt', models.ImageField(upload_to='')),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bid', to='auctions.auction')),
            ],
        ),
    ]
