from django import forms
from .models import Planet

class PlanetForm(forms.ModelForm):
    class Meta:
        model = Planet
        fields = [
            'name', 'image', 'description', 'distance_from_sun', 'radius',
            'gravity', 'day_length', 'atmosphere', 'temperature',
            'category', 'moons_count'
        ]
