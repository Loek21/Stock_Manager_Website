# Generated by Django 2.2.7 on 2019-12-10 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('holding', '0010_auto_20191210_1223'),
    ]

    operations = [
        migrations.RenameField(
            model_name='holding',
            old_name='downh',
            new_name='updownh',
        ),
        migrations.RemoveField(
            model_name='holding',
            name='uph',
        ),
    ]
