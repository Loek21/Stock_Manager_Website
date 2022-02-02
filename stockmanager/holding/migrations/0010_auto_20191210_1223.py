# Generated by Django 2.2.7 on 2019-12-10 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('holding', '0009_realtime_lastpricep'),
    ]

    operations = [
        migrations.AddField(
            model_name='holding',
            name='downh',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='holding',
            name='uph',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
            preserve_default=False,
        ),
    ]
