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
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('/', include('Eau.urls')),
    path('signup', views.signup, name="signup"),   
    path('', views.Home, name="Home"), 
    path('show_water/', views.show_water, name="show_water"),
    path('water_monthly_consumption/', views.water_monthly_consumption, name="water_monthly_consumption"),
    path('gaz_monthly_consumption/', views.gaz_monthly_consumption, name="gaz_monthly_consumption"),
    path('energy_monthly_consumption/', views.energy_monthly_consumption, name="energy_monthly_consumption"),
    
    
    path('export_water/', views.get_water, name="export_water"),
    path('export_water_filtered/<int:year>/<int:month>/', views.get_water_filtered, name="export_water_filtered"),

    path('export_xl_munters/', views.export_xl_munters, name="export_xl_munters"),
    path('export_xl_munters_filtered/<int:year>/<int:month>/', views.export_xl_munters_filtered, name="export_xl_munters_filtered"),
    path('munters_monthly_consumption/', views.munters_monthly_consumption, name="munters_monthly_consumption"),
    



    path('export_monthly_water/', views.export_xl_monthly_water, name="export_xl_monthly_water"),
    
    path('export_gas/', views.export_xl_gas, name="export_xl_gas"),
    path('export_gas_filtered/<int:year>/<int:month>/', views.export_xl_gas_filtered, name="export_xl_gas_filtered"),
    path('export_monthly_gas/', views.export_monthly_gas, name="export_monthly_gas"),
    path('export_monthly_energy/', views.export_monthly_energy, name="export_monthly_energy"),
    path('export_monthly_energy_f/<int:year>/', views.export_monthly_energy_f, name="export_monthly_energy_f"),
    path('export_monthly_gas_f/<int:year>/', views.export_monthly_gas_f, name="export_monthly_gas_f"),
    path('export_monthly_water_f/<int:year>/', views.export_monthly_water_f, name="export_monthly_water_f"),



    path('export_monthly_munters/', views.export_monthly_munters, name="export_monthly_munters"),
    path('export_monthly_munters_f/<int:year>/', views.export_monthly_munters_f, name="export_monthly_munters_f"),
    
    
    

    path('export_energy_filtered/<int:year>/<int:month>/', views.export_xl_energy_filtered, name="export_xl_energy_filtered"),


    path('export_energy/', views.export_xl_energy, name="export_xl_energy"),
    
    path('add_water_consumption/', views.add_water_consumption, name="add_water_consumption"),
    path('show_Energy/', views.show_Energy, name="show_Energy"),
    path('add_Energy_consumption/', views.add_Energy_consumption, name="add_Energy_consumption"),
    path('water_consumption_chart/', views.water_consumption_chart, name='water_consumption_chart'),
    path('water_mensuel_chart/', views.monthly_water_chart, name='water_mensuel_chart'),
    path('monthly_munters_chart/', views.monthly_munters_chart, name='monthly_munters_chart'),
    path('water_mconsumption_chart/', views.water_mconsumption_chart, name='water_mconsumption_chart'),
    path('water_mconsumptionchart/', views.water_mconsumptionchart, name='water_mconsumptionchart'),
    path('gas_mconsumption_chart/', views.gas_mconsumption_chart, name='gas_mconsumption_chart'),
    path('energy_mconsumption_chart/', views.energy_mconsumption_chart, name='energy_mconsumption_chart'),

    path('munters_consumption_chart/', views.munters_consumption_chart, name='munters_consumption_chart'),
    
    path('munters_mconsumption_chart/', views.munters_mconsumption_chart, name='munters_mconsumption_chart'),
    

    #path('cleanmunters/', views.delete_everything, name='delete_everything'),
    

    path('api_water_monthly/', views.api_water_monthly, name='api_water_monthly'),

    path('api_water_monthly_filtered/<int:year>/', views.api_water_monthly_filtered, name='api_water_monthly_filtered'),
    path('api_energy_monthly_filtered/<int:year>/', views.api_energy_monthly_filtered, name='api_energy_monthly_filtered'),
    path('api_gaz_monthly_filtered/<int:year>/', views.api_gaz_monthly_filtered, name='api_gaz_monthly_filtered'),
    path('api_munters_monthly_filtered/<int:year>/', views.api_munters_monthly_filtered, name='api_munters_monthly_filtered'),

    

    path('api_gas_monthly/', views.api_gas_monthly, name='api_gas_monthly'),
    path('api_energy_monthly/', views.api_energy_monthly, name='api_energy_monthly'),

    

    path('energy_consumption_chart/', views.energy_consumption_chart, name='energy_consumption_chart'),
    path('energy_mensuel_chart/', views.monthly_energy_chart, name='energy_mensuel_chart'),
    path('show_monthly_water/', views.show_monthly_water, name="show_monthly_water"),
    path('add_water_monthly_consumption/', views.add_water_monthly_consumption, name="add_water_monthly_consumption"),
    path('water_consumption_monthly_chart/', views.water_consumption_monthly_chart, name='water_consumption_monthly_chart'),
    path('get_consumption_data/', views.get_consumption_data, name='get_consumption_data'),
    path('add_munters_consumption/', views.add_munters_consumption, name='add_munters_consumption'),
    path('show_munters/', views.show_munters, name='show_munters'),
    #path('munters_chart/', views.munters, name='munters_chart'),
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
        path('', views.show_Gas, name='show_Gas'),
        path('modify_gas/<int:id>/', views.modify_gas, name='modify_gas'),
    ])),
    path('delete_gas/<int:id>/', views.delete_gas, name='delete_gas'),
    path('delete_munters/<int:id>/', views.delete_munters, name='delete_munters'),
    
    path('show_monthly_gas/', include([
        path('', views.show_monthly_gas, name='show_monthly_gas'),
        path('modify_gas_monthly/<int:id>/', views.modify_gas_monthly, name='modify_gas_monthly'),
    ])),
    path('delete_monthly_gas/<int:id>/', views.delete_gas_monthly, name='delete_gas_monthly'),
    #path('show_munters_elec/', include([
        #path('', views.show_monthly_gas, name='show_munters_elec'),
        #path('modify_munters_monthly/<int:id>/', views.modify_munters_monthly, name='modify_munters_monthly'),
    #])),
    #path('delete_monthly_munters/<int:id>/', views.delete_munters_monthly, name='delete_munters_monthly'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('factures/', include("factures.urls")),
    path('add_process/', fviews.add_process, name='add_process'),
    path('process/', fviews.get_process, name="process"),
    path('deleteprocess/<int:pk>', fviews.delete_process, name="delete_process"),
    

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)



