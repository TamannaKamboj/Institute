# Generated by Django 3.1 on 2021-03-09 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp1', '0002_auto_20210228_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='fees_cycle',
            field=models.IntegerField(default=6),
            preserve_default=False,
        ),
    ]
