from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import FlightPlanForm
from .models import FlightPlan
from .utils import calculate_distance

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

def flight_detail(request, flight_id):
    flight = get_object_or_404(FlightPlan, id=flight_id)
    return render(request, 'flight_planner/flight_detail.html', {'flight': flight})