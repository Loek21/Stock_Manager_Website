# Generated by Django 2.2.7 on 2019-12-05 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('holding', '0003_realtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realtime',
            name='date',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='realtime',
            name='updated',
            field=models.CharField(max_length=60),
        ),
    ]
