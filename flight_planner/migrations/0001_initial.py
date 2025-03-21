# Generated by Django 5.1.7 on 2025-03-14 22:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aircraft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('manufacturer', models.CharField(max_length=100)),
                ('fuel_burn', models.FloatField(help_text='Fuel burn in lbs/hour')),
                ('cruise_speed', models.FloatField(help_text='Cruise speed in knots')),
            ],
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icao_code', models.CharField(max_length=4, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='FlightPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fuel_required', models.FloatField()),
                ('distance', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('aircraft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight_planner.aircraft')),
                ('arrival', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrival_flights', to='flight_planner.airport')),
                ('departure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departure_flights', to='flight_planner.airport')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
