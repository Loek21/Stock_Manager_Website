# Generated by Django 2.2.7 on 2019-12-11 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('holding', '0020_auto_20191211_1441'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reminder',
            old_name='v',
            new_name='value',
        ),
    ]
