# Generated by Django 2.2.7 on 2019-12-06 10:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_auto_20191205_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='holding',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='holdings', to='holding.Holding'),
        ),
    ]
