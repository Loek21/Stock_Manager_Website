# Generated by Django 2.2.7 on 2019-12-11 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('holding', '0016_auto_20191211_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realtime',
            name='date',
            field=models.CharField(max_length=60),
        ),
    ]
