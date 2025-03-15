from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('plan/', views.plan_flight, name='plan_flight'),
    path('flight/<int:flight_id>/', views.flight_detail, name='flight_detail'),
    path('flight/<int:flight_id>/map/', views.flight_map, name='flight_map'), 
]