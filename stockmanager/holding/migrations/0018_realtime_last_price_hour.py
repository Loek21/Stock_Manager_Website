# Generated by Django 2.2.7 on 2019-12-11 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('holding', '0017_auto_20191211_1041'),
    ]

    operations = [
        migrations.AddField(
            model_name='realtime',
            name='last_price_hour',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
