# Generated by Django 2.2.7 on 2019-12-06 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('holding', '0007_holding_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='holding',
            name='hnamef',
            field=models.CharField(default=0, max_length=60),
            preserve_default=False,
        ),
    ]