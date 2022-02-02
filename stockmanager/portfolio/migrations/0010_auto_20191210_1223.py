# Generated by Django 2.2.7 on 2019-12-10 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0009_remove_portfolio_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='downp',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='portfolio',
            name='upp',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
            preserve_default=False,
        ),
    ]
