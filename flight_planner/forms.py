from django import forms
from .models import FlightPlan, Airport, Aircraft

class FlightPlanForm(forms.ModelForm):
    class Meta:
        model = FlightPlan
        fields = ['departure', 'arrival', 'aircraft']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['departure'].queryset = Airport.objects.all()
        self.fields['arrival'].queryset = Airport.objects.all()
        self.fields['aircraft'].queryset = Aircraft.objects.all()