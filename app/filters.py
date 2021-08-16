from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Count
import django_filters
from django_filters import CharFilter
from django.forms.widgets import TextInput

class actividades_filter(django_filters.FilterSet):

    año = CharFilter(field_name='año', label='Año', lookup_expr='icontains', widget=TextInput(attrs={'size':4}))
    mes = CharFilter(field_name='mes', label='Mes', lookup_expr='icontains', widget=TextInput(attrs={'size':4}))
    dia = CharFilter(field_name='dia', label='Dia', lookup_expr='icontains', widget=TextInput(attrs={'size':4}))

    class Meta:
        model = actividades
        fields = ['atleta','año','mes','dia','tipo']