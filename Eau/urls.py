from django.contrib import admin
from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.Home, name="Home"),
    path('Home', views.Home, name="Home"),    
    path('show_water/', views.show_water, name="show_water"),
    path('add_water_consumption/', views.add_water_consumption, name="add_water_consumption"),
    path('show_Energy/', views.show_Energy, name="show_Energy"),
    path('add_Energy_consumption/', views.add_Energy_consumption, name="add_Energy_consumption"),
    path('water_consumption_chart/', views.water_consumption_chart, name='water_consumption_chart'),
    path('water_mensuel_chart/', views.monthly_water_chart, name='water_mensuel_chart'),
    path('energy_consumption_chart/', views.energy_consumption_chart, name='energy_consumption_chart'),
    path('energy_mensuel_chart/', views.monthly_energy_chart, name='energy_mensuel_chart'),
    path('show_monthly_water/', views.show_monthly_water, name="show_monthly_water"),
    path('add_water_monthly_consumption/', views.add_water_monthly_consumption, name="add_water_monthly_consumption"),
    path('water_consumption_monthly_chart/', views.water_consumption_monthly_chart, name='water_consumption_monthly_chart'),
    path('get_consumption_data/', views.get_consumption_data, name='get_consumption_data'),
    path('add_munters_consumption/', views.add_munters_consumption, name='add_munters_consumption'),
    path('show_munters_elec/', views.show_munters_elec, name='show_munters_elec'),
    path('munters_chart/', views.munters, name='munters_chart'),
    path('water_anual_compare_chart/', views.water_anual_compare_chart, name='water_anual_compare_chart'),
    path('compare/', views.show_compare_by_years, name='compare-by-years'),
    path('add_machine/', views.add_machine, name='add_machine'),
    path('show_machines/', views.show_machines, name='show_machines'),
    path('add_gas_consumption/', views.add_gas_consumption, name="add_gas_consumption"),
    path('add_gas_monthly_consumption/', views.add_gas_monthly_consumption, name="add_gas_monthly_consumption"),
    path('show_Gas/', views.show_Gas, name="show_Gas"),
    path('show_monthly_gas/', views.show_monthly_gas, name="show_monthly_gas"),
    path('gas_consumption_chart/', views.gas_consumption_chart, name='gas_consumption_chart'),
    path('gas_mensuel_chart/', views.monthly_gas_chart, name='gas_mensuel_chart'),
    path('gas_consumption_monthly_chart/', views.gas_consumption_monthly_chart, name='gas_consumption_monthly_chart'),
    path('get_consumption_data_gas/', views.get_consumption_data_gas, name='get_consumption_data_gas'),
    path('gas_anual_compare_chart/', views.gas_anual_compare_chart, name='gas_anual_compare_chart'),
    path('compare_anual_gas/', views.show_compare_by_years_gas, name='show_compare_by_years_gas'),
    



]