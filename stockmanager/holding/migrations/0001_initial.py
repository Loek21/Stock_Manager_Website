# Generated by Django 2.2.7 on 2019-12-02 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Holding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hname', models.CharField(max_length=60)),
                ('hnumber', models.IntegerField()),
                ('hvalue', models.DecimalField(decimal_places=2, max_digits=11)),
                ('hvaluep', models.DecimalField(decimal_places=2, max_digits=11)),
            ],
        ),
    ]
