# Generated by Django 2.2.7 on 2019-12-06 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_auto_20191206_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='holding',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='holding.Holding'),
        ),
    ]
