# Generated by Django 2.2.7 on 2019-12-06 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('holding', '0006_realtime_lastprice'),
        ('portfolio', '0006_auto_20191206_1328'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfolio',
            name='holding',
        ),
        migrations.AddField(
            model_name='portfolio',
            name='content',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='holding.Holding'),
        ),
    ]