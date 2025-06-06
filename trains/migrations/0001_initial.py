# Generated by Django 5.2.1 on 2025-05-10 14:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('number', models.CharField(max_length=10, unique=True)),
                ('source', models.CharField(max_length=100)),
                ('destination', models.CharField(max_length=100)),
                ('train_type', models.CharField(choices=[('Express', 'Express'), ('Superfast', 'Superfast'), ('Passenger', 'Passenger'), ('Intercity', 'Intercity')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('departure_time', models.TimeField()),
                ('arrival_time', models.TimeField()),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='trains.train')),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station_name', models.CharField(max_length=100)),
                ('arrival_time', models.TimeField()),
                ('departure_time', models.TimeField()),
                ('stop_number', models.PositiveIntegerField()),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routes', to='trains.train')),
            ],
            options={
                'ordering': ['stop_number'],
            },
        ),
    ]
