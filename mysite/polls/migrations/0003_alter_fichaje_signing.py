# Generated by Django 5.0.6 on 2024-05-29 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_rename_club_club_club_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fichaje',
            name='signing',
            field=models.DateField(null=True),
        ),
    ]