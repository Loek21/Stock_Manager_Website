# Generated by Django 2.2.7 on 2019-12-10 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0011_auto_20191210_1229'),
    ]

    operations = [
        migrations.RenameField(
            model_name='portfolio',
            old_name='updownp',
            new_name='updownpp',
        ),
        migrations.AddField(
            model_name='portfolio',
            name='updownpv',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=11),
            preserve_default=False,
        ),
    ]
