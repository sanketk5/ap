# Generated by Django 3.0.1 on 2020-09-25 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_auto_20200925_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='authors',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='book',
            name='edition',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='bookrequests',
            name='authors',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='bookrequests',
            name='ideal_course',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='bookrequests',
            name='ideal_sem',
            field=models.CharField(max_length=150),
        ),
    ]
