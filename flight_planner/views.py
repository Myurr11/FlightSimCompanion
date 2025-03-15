from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import FlightPlanForm
from .models import FlightPlan
from .utils import calculate_distance
import requests
import folium
from folium.plugins import AntPath
from django.conf import settings

def home(request):
    if request.user.is_authenticated:
        flight_plans = FlightPlan.objects.filter(user=request.user)
    else:
        flight_plans = []
    return render(request, 'flight_planner/home.html', {'flight_plans': flight_plans})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def plan_flight(request):
    if request.method == 'POST':
        form = FlightPlanForm(request.POST)
        if form.is_valid():
            flight_plan = form.save(commit=False)
            flight_plan.user = request.user

            # Calculate distance
            departure = flight_plan.departure
            arrival = flight_plan.arrival
            distance = calculate_distance(
                departure.latitude, departure.longitude,
                arrival.latitude, arrival.longitude
            )

            # Calculate fuel required
            aircraft = flight_plan.aircraft
            flight_plan.distance = distance
            flight_plan.fuel_required = distance * aircraft.fuel_burn  # Example calculation

            flight_plan.save()
            return redirect('home')
    else:
        form = FlightPlanForm()
    return render(request, 'flight_planner/plan_flight.html', {'form': form})

def get_weather(lat, lon):
    api_key = settings.OPENWEATHERMAP_API_KEY  # Use the API key from settings
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def flight_detail(request, flight_id):
    flight = get_object_or_404(FlightPlan, id=flight_id)

    # Get weather for departure and arrival airports
    departure_weather = get_weather(flight.departure.latitude, flight.departure.longitude)
    arrival_weather = get_weather(flight.arrival.latitude, flight.arrival.longitude)

    # Create a map centered between the departure and arrival airports
    map_center = [
        (flight.departure.latitude + flight.arrival.latitude) / 2,
        (flight.departure.longitude + flight.arrival.longitude) / 2,
    ]
    flight_map = folium.Map(location=map_center, zoom_start=4)

    # Add markers for departure and arrival airports
    folium.Marker(
        [flight.departure.latitude, flight.departure.longitude],
        tooltip=f"Departure: {flight.departure}",
    ).add_to(flight_map)

    folium.Marker(
        [flight.arrival.latitude, flight.arrival.longitude],
        tooltip=f"Arrival: {flight.arrival}",
    ).add_to(flight_map)

    # Add a line connecting the departure and arrival airports
    AntPath(
        locations=[
            [flight.departure.latitude, flight.departure.longitude],
            [flight.arrival.latitude, flight.arrival.longitude],
        ],
        color='blue',
        dash_array=[10, 20],
    ).add_to(flight_map)

    # Render the map to HTML
    flight_map = flight_map._repr_html_()  # Convert the map to HTML

    return render(request, 'flight_planner/flight_detail.html', {
        'flight': flight,
        'departure_weather': departure_weather,
        'arrival_weather': arrival_weather,
        'flight_map': flight_map,  # Pass the map HTML to the template
    })

def flight_map(request, flight_id):
    flight = get_object_or_404(FlightPlan, id=flight_id)

    # Create a map centered between the departure and arrival airports
    map_center = [
        (flight.departure.latitude + flight.arrival.latitude) / 2,
        (flight.departure.longitude + flight.arrival.longitude) / 2,
    ]
    flight_map = folium.Map(location=map_center, zoom_start=4)

    # Add markers for departure and arrival airports
    folium.Marker(
        [flight.departure.latitude, flight.departure.longitude],
        tooltip=f"Departure: {flight.departure}",
    ).add_to(flight_map)

    folium.Marker(
        [flight.arrival.latitude, flight.arrival.longitude],
        tooltip=f"Arrival: {flight.arrival}",
    ).add_to(flight_map)

    # Add a line connecting the departure and arrival airports
    AntPath(
        locations=[
            [flight.departure.latitude, flight.departure.longitude],
            [flight.arrival.latitude, flight.arrival.longitude],
        ],
        color='blue',
        dash_array=[10, 20],
    ).add_to(flight_map)

    # Render the map to HTML
    flight_map_html = flight_map._repr_html_()

    return render(request, 'flight_planner/flight_map.html', {
        'flight_map': flight_map_html,
        'flight': flight,  # Pass the flight object to the template
    })