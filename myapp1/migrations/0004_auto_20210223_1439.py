# Generated by Django 3.1 on 2021-02-23 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp1', '0003_auto_20210219_2251'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=23)),
                ('rollno', models.IntegerField()),
                ('stu_class', models.CharField(max_length=23)),
                ('f_name', models.CharField(max_length=23)),
                ('m_name', models.CharField(max_length=23)),
                ('dateOfBirth', models.DateTimeField()),
                ('address', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='email',
            field=models.CharField(default='test@test.com', max_length=23),
            preserve_default=False,
        ),
    ]