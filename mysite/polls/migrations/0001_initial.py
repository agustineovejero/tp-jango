# Generated by Django 5.0.6 on 2024-06-11 23:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=100)),
                ('age', models.IntegerField(null=True)),
                ('height', models.FloatField(null=True)),
                ('preferred_foot', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Signing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_signed', models.DateField(null=True)),
                ('previous_team', models.CharField(max_length=100, null=True)),
                ('market_value', models.IntegerField(null=True)),
                ('season', models.CharField(max_length=10, null=True)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.club')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.player')),
            ],
        ),
    ]
