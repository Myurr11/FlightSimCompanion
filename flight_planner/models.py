from django.db import models

class Airport(models.Model):
    icao_code = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.icao_code})"

class Aircraft(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    fuel_burn = models.FloatField(help_text="Fuel burn in lbs/hour")
    cruise_speed = models.FloatField(help_text="Cruise speed in knots")

    def __str__(self):
        return self.name

class FlightPlan(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    departure = models.ForeignKey(Airport, related_name='departure_flights', on_delete=models.CASCADE)
    arrival = models.ForeignKey(Airport, related_name='arrival_flights', on_delete=models.CASCADE)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    fuel_required = models.FloatField()
    distance = models.FloatField()  # Add this field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Flight from {self.departure} to {self.arrival}"