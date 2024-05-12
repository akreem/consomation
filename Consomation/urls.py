"""Consomation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Eau import views
from factures import views as fviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('/', include('Eau.urls')),
    path('', views.signup, name="signup"),   
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
    path('daily-consumption/', views.get_daily_consumption, name='daily-consumption'),
    path('show_monthly_energy/', views.show_monthly_energy, name="show_monthly_energy"),
    path('add_energy_monthly_consumption/', views.add_energy_monthly_consumption, name="add_energy_monthly_consumption"),
    path('energy_consumption_monthly_chart/', views.energy_consumption_monthly_chart, name='energy_consumption_monthly_chart'),
    path('get_consumption_data_energy/', views.get_consumption_data_energy, name='get_consumption_data_energy'),
    path('energy_anual_compare_chart/', views.energy_anual_compare_chart, name='energy_anual_compare_chart'),
    path('compare_anual_energy/', views.show_compare_by_years_energy, name='show_compare_by_years_energy'),
    path('show_water/', include([
        path('', views.show_water, name='show_water'),
        path('modify_water/<int:id>/', views.modify_water, name='modify_water'),
    ])),
    path('delete/<int:id>/', views.delete_water, name='delete_water'),
    path('show_monthly_water/', include([
        path('', views.show_water, name='show_monthly_water'),
        path('modify_water_monthly/<int:id>/', views.modify_water_monthly, name='modify_water_monthly'),
    ])),
    path('delete_monthly/<int:id>/', views.delete_water_monthly, name='delete_water_monthly'),
    path('show_Energy/', include([
        path('', views.show_water, name='show_Energy'),
        path('modify_energy/<int:id>/', views.modify_energy, name='modify_energy'),
    ])),
    path('delete_energy/<int:id>/', views.delete_energy, name='delete_energy'),
    path('show_monthly_energy/', include([
        path('', views.show_monthly_energy, name='show_monthly_energy'),
        path('modify_energy_monthly/<int:id>/', views.modify_energy_monthly, name='modify_energy_monthly'),
    ])),
    path('delete_monthly_energy/<int:id>/', views.delete_energy_monthly, name='delete_energy_monthly'),

    path('show_Gas', include([
        path('', views.show_water, name='show_Gas'),
        path('modify_gas/<int:id>/', views.modify_gas, name='modify_gas'),
    ])),
    path('delete_gas/<int:id>/', views.delete_gas, name='delete_gas'),
    path('show_monthly_gas/', include([
        path('', views.show_monthly_gas, name='show_monthly_gas'),
        path('modify_gas_monthly/<int:id>/', views.modify_gas_monthly, name='modify_gas_monthly'),
    ])),
    path('delete_monthly_gas/<int:id>/', views.delete_gas_monthly, name='delete_gas_monthly'),
    path('show_munters_elec/', include([
        path('', views.show_monthly_gas, name='show_munters_elec'),
        path('modify_munters_monthly/<int:id>/', views.modify_munters_monthly, name='modify_munters_monthly'),
    ])),
    path('delete_monthly_munters/<int:id>/', views.delete_munters_monthly, name='delete_munters_monthly'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('factures/', include("factures.urls")),
    path('add_process/', fviews.add_process, name='add_process'),
    path('process/', fviews.get_process, name="get_process"),
    path('deleteprocess/<int:pk>', fviews.delete_process, name="delete_process"),
    

]



