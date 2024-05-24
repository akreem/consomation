from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from .models import WaterConsumption,EnergyConsumption,WaterMonthlyConsumption,MuntersConsumption, Machines,GasConsumption,GasMonthlyConsumption,EnergyMonthlyConsumption
from collections import defaultdict
from itertools import groupby
from django.http import JsonResponse 
from django.db.models.functions import ExtractMonth, ExtractYear
from django.db.models import Sum, F
from django.db.models.functions import TruncMonth, TruncDay
from collections import OrderedDict
from django.contrib import messages
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from django.urls import reverse
from django.shortcuts import  get_object_or_404
from django.contrib import messages
from django.db.models import Min, Max
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from openpyxl import Workbook
from django.core import serializers

#def delete_everything(self):
    #Munters.objects.all().delete()
    #return HttpResponse('done')

## HOME PAGE ##

@login_required(login_url='login')
def Home(request):
   return render(request, "index.html")

## END HOME PAGE ##

## AUTHENTIFICATION ##
def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, 'Signup successful!')
                return redirect('/')
            else:
                for msg in form.error_messages:
                    messages.error(request, f"{msg}: {form.error_messages[msg]}")
        else:
            form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('Home')
        else:
            form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')

## END AUTHENTIFICATION ##


### INSERTION OF RECORDS ###

""" @login_required(login_url='login')
def add_water_consumption(request):
    if request.method == 'POST':
        # Extraire les données de la requête POST
        date_str = request.POST.get('date')
        meter_reading = int(request.POST.get('meter_reading'))

        # Convertir la chaîne de date en objet datetime
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

        # Trouver le dernier relevé de compteur avant la date actuelle
        last_record = WaterConsumption.objects.filter().order_by('-date').first()

        # Vérifier si le nouveau relevé de compteur est supérieur au dernier relevé de compteur
        if last_record :
            expected_next_date = last_record.date + timedelta(days=1)
            if date_obj < expected_next_date:
                messages.error(request, f'La date {date_obj} du nouvel enregistrement est trop ancienne, vous devez saisir une nouvelle date supérieure à {last_record.date}. La prochaine date prévue est le {expected_next_date}."')
                return render(request, "Eau.html", {
                        'date': date_str,
                        'meter_reading': meter_reading,
                    })
            elif date_obj > expected_next_date:
                messages.error(request, f'Vous devez d"abord saisir les données de l"enregistrement avec la date {expected_next_date}."')
                return render(request, "Eau.html", {
                        'date': date_str,
                        'meter_reading': meter_reading,
                    })
            else:
                if meter_reading <= last_record.meter_reading :
                    # Si ce n'est pas le cas, afficher un message d'erreur et rendre le formulaire à nouveau
                    messages.error(request, 'La nouvelle valeur du compteur doit être supérieure à la dernière valeur enregistrée.')
                    return render(request, "Eau.html", {
                        'date': date_str,
                        'meter_reading': meter_reading,
                    })

        # Calculer la consommation journalière en utilisant la différence de prélèvement
        if last_record:
            last_daily_consumption = meter_reading - last_record.meter_reading

            last_record.daily_consumption = last_daily_consumption
            last_record.save()

            
            new_record = WaterConsumption.objects.create(
            date=date_obj,
            meter_reading=meter_reading ,
            daily_consumption= 0
            )
            redirect_url = reverse('show_water')
            return redirect(redirect_url)
        else:
            new_record = WaterConsumption.objects.create(
            date=date_obj,
            meter_reading=meter_reading ,
            daily_consumption= 0
            )
            redirect_url = reverse('show_water')
            return redirect(redirect_url)
    return render(request, "Eau.html") """


@login_required(login_url='login')
def add_water_consumption(request):
    if request.method == 'POST':
        # Extraire les données de la requête POST
        date_str = request.POST.get('date')
        meter_reading = int(request.POST.get('meter_reading'))

        # Convertir la chaîne de date en objet datetime
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

        is_date_registered = WaterConsumption.objects.filter(date=date_obj).exists()
        if is_date_registered:
            messages.error(request, f'le nouvel enregistrement avec la date {date_obj} existe déjà')
            return render(request, "Eau.html", {
                'date': date_str,
                'meter_reading': meter_reading,
            })
        else :


            # Trouver le dernier relevé de compteur avant la date actuelle
            #previous_row = WaterConsumption.objects.filter(date__lt=date_str).order_by('-date').first()

            last_record = WaterConsumption.objects.filter(date__lt=date_str).order_by('-date').first()
            next_record = WaterConsumption.objects.filter(date__gt=date_str).order_by('date').first()

            #last_record = WaterConsumption.objects.filter().order_by('-date').first()

            # Calculer la consommation journalière en utilisant la différence de prélèvement
            if last_record:
                if meter_reading <= last_record.meter_reading :
                        # Si ce n'est pas le cas, afficher un message d'erreur et rendre le formulaire à nouveau
                        messages.error(request, 'La nouvelle valeur du compteur doit être supérieure à la dernière valeur enregistrée.')
                        return render(request, "Eau.html", {
                            'date': date_str,
                            'meter_reading': meter_reading,
                        })
                elif next_record:

                    last_record.daily_consumption = meter_reading - last_record.meter_reading
                    last_record.save()

                    new_record = WaterConsumption.objects.create(
                    date=date_obj,
                    meter_reading=meter_reading ,
                    daily_consumption= next_record.meter_reading - meter_reading
                    )
                    redirect_url = reverse('show_water')
                    return redirect(redirect_url)

                else : 
                    last_daily_consumption = meter_reading - last_record.meter_reading

                    last_record.daily_consumption = last_daily_consumption
                    last_record.save()

                    
                    new_record = WaterConsumption.objects.create(
                    date=date_obj,
                    meter_reading=meter_reading ,
                    daily_consumption= 0
                    )
                    redirect_url = reverse('show_water')
                    return redirect(redirect_url)
            else:
                if next_record:
                    if meter_reading >= next_record.meter_reading :
                        # Si ce n'est pas le cas, afficher un message d'erreur et rendre le formulaire à nouveau
                        messages.error(request, 'La nouvelle valeur du compteur doit être inférieur à la prochaine valeur enregistrée.')
                        return render(request, "Eau.html", {
                            'date': date_str,
                            'meter_reading': meter_reading,
                        })
                    else : 
                        new_record = WaterConsumption.objects.create(
                        date=date_obj,
                        meter_reading=meter_reading ,
                        daily_consumption= next_record.meter_reading - meter_reading
                        )
                        redirect_url = reverse('show_water')
                        return redirect(redirect_url)

                else:
                    new_record = WaterConsumption.objects.create(
                    date=date_obj,
                    meter_reading=meter_reading ,
                    daily_consumption= 0
                    )
                    redirect_url = reverse('show_water')
                    return redirect(redirect_url)
    return render(request, "Eau.html")


def delete_water(request, id):
    consumption = get_object_or_404(WaterConsumption, pk=id)
    previous_row = WaterConsumption.objects.filter(date__lt=consumption.date).order_by('-date').first()

    if previous_row:
        previous_row.daily_consumption = 0
        previous_row.save()

    consumption.delete()

    redirect_url = reverse('show_water')
    return redirect(redirect_url)


@login_required(login_url='login')
def add_gas_consumption(request):
    if request.method == 'POST':
        # Extraire les données de la requête POST
        date_str = request.POST.get('date')
        meter_reading = int(request.POST.get('meter_reading'))

        # Convertir la chaîne de date en objet datetime
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

        is_date_registered = GasConsumption.objects.filter(date=date_obj).exists()
        if is_date_registered:
            messages.error(request, f'le nouvel enregistrement avec la date {date_obj} existe déjà')
            return render(request, "gas.html", {
                'date': date_str,
                'meter_reading': meter_reading,
            })
        else :


            # Trouver le dernier relevé de compteur avant la date actuelle
            #previous_row = WaterConsumption.objects.filter(date__lt=date_str).order_by('-date').first()

            last_record = GasConsumption.objects.filter(date__lt=date_str).order_by('-date').first()
            next_record = GasConsumption.objects.filter(date__gt=date_str).order_by('date').first()

            #last_record = WaterConsumption.objects.filter().order_by('-date').first()

            # Calculer la consommation journalière en utilisant la différence de prélèvement
            if last_record:
                if meter_reading <= last_record.meter_reading :
                        # Si ce n'est pas le cas, afficher un message d'erreur et rendre le formulaire à nouveau
                        messages.error(request, 'La nouvelle valeur du compteur doit être supérieure à la dernière valeur enregistrée.')
                        return render(request, "gas.html", {
                            'date': date_str,
                            'meter_reading': meter_reading,
                        })
                elif next_record:

                    last_record.daily_consumption = meter_reading - last_record.meter_reading
                    last_record.save()

                    new_record = GasConsumption.objects.create(
                    date=date_obj,
                    meter_reading=meter_reading ,
                    daily_consumption= next_record.meter_reading - meter_reading
                    )
                    redirect_url = reverse('show_gas')
                    return redirect(redirect_url)

                else : 
                    last_daily_consumption = meter_reading - last_record.meter_reading

                    last_record.daily_consumption = last_daily_consumption
                    last_record.save()

                    
                    new_record = GasConsumption.objects.create(
                    date=date_obj,
                    meter_reading=meter_reading ,
                    daily_consumption= 0
                    )
                    redirect_url = reverse('show_gas')
                    return redirect(redirect_url)
            else:
                if next_record:
                    if meter_reading >= next_record.meter_reading :
                        # Si ce n'est pas le cas, afficher un message d'erreur et rendre le formulaire à nouveau
                        messages.error(request, 'La nouvelle valeur du compteur doit être inférieur à la prochaine valeur enregistrée.')
                        return render(request, "gas.html", {
                            'date': date_str,
                            'meter_reading': meter_reading,
                        })
                    else : 
                        new_record = GasConsumption.objects.create(
                        date=date_obj,
                        meter_reading=meter_reading ,
                        daily_consumption= next_record.meter_reading - meter_reading
                        )
                        redirect_url = reverse('show_gas')
                        return redirect(redirect_url)

                else:
                    new_record = GasConsumption.objects.create(
                    date=date_obj,
                    meter_reading=meter_reading ,
                    daily_consumption= 0
                    )
                    redirect_url = reverse('show_gas')
                    return redirect(redirect_url)
    return render(request, "gas.html")


def delete_gas(request, id):
    consumption = get_object_or_404(GasConsumption, pk=id)
    previous_row = GasConsumption.objects.filter(date__lt=consumption.date).order_by('-date').first()

    if previous_row:
        previous_row.daily_consumption = 0
        previous_row.save()

    consumption.delete()

    redirect_url = reverse('show_Gas')
    return redirect(redirect_url)




""" login_required(login_url='login')
def add_gas_consumption(request):
    if request.method == 'POST':
        # Extraire les données de la requête POST
        date_str = request.POST.get('date')
        meter_reading = int(request.POST.get('meter_reading'))

        # Convertir la chaîne de date en objet datetime
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

        # Trouver le dernier relevé de compteur avant la date actuelle

        last_record = GasConsumption.objects.filter().order_by('-date').first()

        if last_record :
            expected_next_date = last_record.date + timedelta(days=1)
            if date_obj < expected_next_date:
                messages.error(request, f'La date {date_obj} du nouvel enregistrement est trop ancienne, vous devez saisir une nouvelle date supérieure à {last_record.date}. La prochaine date prévue est le {expected_next_date}."')
                return render(request, "gas.html", {
                        'date': date_str,
                        'meter_reading': meter_reading,
                    })
            elif date_obj > expected_next_date:
                messages.error(request, f'Vous devez d"abord saisir les données de l"enregistrement avec la date {expected_next_date}."')
                return render(request, "gas.html", {
                        'date': date_str,
                        'meter_reading': meter_reading,
                    })
            else:
                if meter_reading <= last_record.meter_reading :
                    # Si ce n'est pas le cas, afficher un message d'erreur et rendre le formulaire à nouveau
                    messages.error(request, 'La nouvelle valeur du compteur doit être supérieure à la dernière valeur enregistrée.')
                    return render(request, "gas.html", {
                        'date': date_str,
                        'meter_reading': meter_reading,
                    })

        # Calculer la consommation journalière en utilisant la différence de prélèvement
        if last_record:
            last_daily_consumption = meter_reading - last_record.meter_reading
            last_record.daily_consumption = last_daily_consumption
            last_record.save()

            new_record = GasConsumption.objects.create(
            date=date_obj,
            meter_reading=meter_reading,
            daily_consumption = 0
            )
            redirect_url = reverse('show_Gas')
            return redirect(redirect_url)


        else:
            new_record = GasConsumption.objects.create(
            date=date_obj,
            meter_reading=meter_reading,
            daily_consumption = 0
            )
            redirect_url = reverse('show_Gas')
            return redirect(redirect_url)
    return render(request, "gas.html") """


@login_required(login_url='login')
def add_Energy_consumption(request):
    if request.method == 'POST':
        # Extraire les données de la requête POST
        date_str = request.POST.get('date')
        meter_reading = int(request.POST.get('meter_reading'))

        # Convertir la chaîne de date en objet datetime
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

        is_date_registered = EnergyConsumption.objects.filter(date=date_obj).exists()
        if is_date_registered:
            messages.error(request, f'le nouvel enregistrement avec la date {date_obj} existe déjà')
            return render(request, "energy.html", {
                'date': date_str,
                'meter_reading': meter_reading,
            })
        else :

            # Trouver le dernier relevé de compteur avant la date actuelle

            last_record = EnergyConsumption.objects.filter(date__lt=date_str).order_by('-date').first()
            next_record = EnergyConsumption.objects.filter(date__gt=date_str).order_by('date').first()


            # Calculer la consommation journalière en utilisant la différence de prélèvement
            if last_record:
                if meter_reading <= last_record.meter_reading :
                        # Si ce n'est pas le cas, afficher un message d'erreur et rendre le formulaire à nouveau
                        messages.error(request, 'La nouvelle valeur du compteur doit être supérieure à la dernière valeur enregistrée.')
                        return render(request, "energy.html", {
                            'date': date_str,
                            'meter_reading': meter_reading,
                        })
                elif next_record:

                    last_record.daily_consumption = meter_reading - last_record.meter_reading
                    last_record.save()

        # Convertir la chaîne de date en objet datetime
                    new_record = EnergyConsumption.objects.create(
                    date=date_obj,
                    meter_reading=meter_reading ,
                    daily_consumption= next_record.meter_reading - meter_reading
                    )
                    redirect_url = reverse('show_Energy')
                    return redirect(redirect_url)

                else : 
                    last_daily_consumption = meter_reading - last_record.meter_reading

                    last_record.daily_consumption = last_daily_consumption
                    last_record.save()

                    
                    new_record = EnergyConsumption.objects.create(
                    date=date_obj,
                    meter_reading=meter_reading ,
                    daily_consumption= 0
                    )
                    redirect_url = reverse('show_Energy')
                    return redirect(redirect_url)
            else:
                if next_record:
                    if meter_reading >= next_record.meter_reading :
                        # Si ce n'est pas le cas, afficher un message d'erreur et rendre le formulaire à nouveau
                        messages.error(request, 'La nouvelle valeur du compteur doit être inférieur à la prochaine valeur enregistrée.')
                        return render(request, "energy.html", {
                            'date': date_str,
                            'meter_reading': meter_reading,
                        })
                    else : 
                        new_record = EnergyConsumption.objects.create(
                        date=date_obj,
                        meter_reading=meter_reading ,
                        daily_consumption= next_record.meter_reading - meter_reading
                        )
                        redirect_url = reverse('show_Energy')
                        return redirect(redirect_url)

                else:
                    new_record = EnergyConsumption.objects.create(
                    date=date_obj,
                    meter_reading=meter_reading ,
                    daily_consumption= 0
                    )
                    redirect_url = reverse('show_Energy')
                    return redirect(redirect_url)
    return render(request, "energy.html")


def delete_energy(request, id):
    consumption = get_object_or_404(EnergyConsumption, pk=id)
    previous_row = EnergyConsumption.objects.filter(date__lt=consumption.date).order_by('-date').first()

    if previous_row:
        previous_row.daily_consumption = 0
        previous_row.save()

    consumption.delete()

    redirect_url = reverse('show_Energy')
    return redirect(redirect_url)




""" @login_required(login_url='login')
def add_Energy_consumption(request):
    if request.method == 'POST':
        # Extraire les données de la requête POST
        date_str = request.POST.get('date')
        meter_reading = float(request.POST.get('meter_reading'))

        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

        # Trouver le dernier relevé de compteur avant la date actuelle
        last_record = EnergyConsumption.objects.filter().order_by('-date').first()

        if last_record :
            expected_next_date = last_record.date + timedelta(days=1)
            if date_obj < expected_next_date:
                messages.error(request, f'La date {date_obj} du nouvel enregistrement est trop ancienne, vous devez saisir une nouvelle date supérieure à {last_record.date}. La prochaine date prévue est le {expected_next_date}."')
                return render(request, "energy.html", {
                        'date': date_str,
                        'meter_reading': meter_reading,
                    })
            elif date_obj > expected_next_date:
                messages.error(request, f'Vous devez d"abord saisir les données de l"enregistrement avec la date {expected_next_date}."')
                return render(request, "energy.html", {
                        'date': date_str,
                        'meter_reading': meter_reading,
                    })
            else:
                if meter_reading <= last_record.meter_reading :
                    # Si ce n'est pas le cas, afficher un message d'erreur et rendre le formulaire à nouveau
                    messages.error(request, 'La nouvelle valeur du compteur doit être supérieure à la dernière valeur enregistrée.')
                    return render(request, "energy.html", {
                        'date': date_str,
                        'meter_reading': meter_reading,
                    })

        # Calculer la consommation journalière en utilisant la différence de prélèvement
        if last_record:
            last_daily_consumption = meter_reading - last_record.meter_reading
            last_record.daily_consumption = last_daily_consumption
            last_record.save()

            new_record = EnergyConsumption.objects.create(
                date=date_str, meter_reading=meter_reading,
                daily_consumption=0
                )
            redirect_url = reverse('show_Energy')
            return redirect(redirect_url)
        else:
            new_record = EnergyConsumption.objects.create(
                date=date_str, meter_reading=meter_reading,
                daily_consumption=0
                )
            redirect_url = reverse('show_Energy')
            return redirect(redirect_url)
    return render(request, "energy.html") """

""" @login_required(login_url='login')
def add_munters_consumption(request):
    if request.method == 'POST':
        # Extraire les données de la requête POST
        date_str = request.POST.get('date')
        meter_reading = float(request.POST.get('meter_reading'))

        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

        # Trouver le dernier relevé de compteur avant la date actuelle
        last_record = MuntersConsumption.objects.filter().order_by('-date').first()

        if last_record :
            expected_next_date = last_record.date + timedelta(days=1)
            if date_obj < expected_next_date:
                messages.error(request, f'La date {date_obj} du nouvel enregistrement est trop ancienne, vous devez saisir une nouvelle date supérieure à {last_record.date}. La prochaine date prévue est le {expected_next_date}."')
                return render(request, "munters.html", {
                        'date': date_str,
                        'meter_reading': meter_reading,
                    })
            elif date_obj > expected_next_date:
                messages.error(request, f'Vous devez d"abord saisir les données de l"enregistrement avec la date {expected_next_date}."')
                return render(request, "munters.html", {
                        'date': date_str,
                        'meter_reading': meter_reading,
                    })
            else:
                if meter_reading <= last_record.meter_reading :
                    # Si ce n'est pas le cas, afficher un message d'erreur et rendre le formulaire à nouveau
                    messages.error(request, 'La nouvelle valeur du compteur doit être supérieure à la dernière valeur enregistrée.')
                    return render(request, "munters.html", {
                        'date': date_str,
                        'meter_reading': meter_reading,
                    })

        # Calculer la consommation journalière en utilisant la différence de prélèvement
        if last_record:
            last_daily_consumption = meter_reading - last_record.meter_reading
            last_record.daily_consumption = last_daily_consumption
            last_record.save()

            new_record = MuntersConsumption.objects.create(
                date=date_str, meter_reading=meter_reading,
                daily_consumption=0
                )
            redirect_url = reverse('show_munters')
            return redirect(redirect_url)
        else:
            new_record = MuntersConsumption.objects.create(
                date=date_str, meter_reading=meter_reading,
                daily_consumption=0
                )
            redirect_url = reverse('show_munters')
            return redirect(redirect_url)
    return render(request, "munters.html") """



@login_required(login_url='login')
def add_munters_consumption(request):
    if request.method == 'POST':
        # Extraire les données de la requête POST
        date_str = request.POST.get('date')
        meter_reading = int(request.POST.get('meter_reading'))

        # Convertir la chaîne de date en objet datetime
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

        is_date_registered = MuntersConsumption.objects.filter(date=date_obj).exists()
        if is_date_registered:
            messages.error(request, f'le nouvel enregistrement avec la date {date_obj} existe déjà')
            return render(request, "munters.html", {
                'date': date_str,
                'meter_reading': meter_reading,
            })
        else :

            # Trouver le dernier relevé de compteur avant la date actuelle

            last_record = MuntersConsumption.objects.filter(date__lt=date_str).order_by('-date').first()
            next_record = MuntersConsumption.objects.filter(date__gt=date_str).order_by('date').first()


            # Calculer la consommation journalière en utilisant la différence de prélèvement
            if last_record:
                if meter_reading <= last_record.meter_reading :
                        # Si ce n'est pas le cas, afficher un message d'erreur et rendre le formulaire à nouveau
                        messages.error(request, 'La nouvelle valeur du compteur doit être supérieure à la dernière valeur enregistrée.')
                        return render(request, "munters.html", {
                            'date': date_str,
                            'meter_reading': meter_reading,
                        })
                elif next_record:

                    last_record.daily_consumption = meter_reading - last_record.meter_reading
                    last_record.save()

                    new_record = MuntersConsumption.objects.create(
                    date=date_obj,
                    meter_reading=meter_reading ,
                    daily_consumption= next_record.meter_reading - meter_reading
                    )
                    redirect_url = reverse('show_munters')
                    return redirect(redirect_url)

                else : 
                    last_daily_consumption = meter_reading - last_record.meter_reading

                    last_record.daily_consumption = last_daily_consumption
                    last_record.save()

                    
                    new_record = MuntersConsumption.objects.create(
                    date=date_obj,
                    meter_reading=meter_reading ,
                    daily_consumption= 0
                    )
                    redirect_url = reverse('show_munters')
                    return redirect(redirect_url)
            else:
                if next_record:
                    if meter_reading >= next_record.meter_reading :
                        # Si ce n'est pas le cas, afficher un message d'erreur et rendre le formulaire à nouveau
                        messages.error(request, 'La nouvelle valeur du compteur doit être inférieur à la prochaine valeur enregistrée.')
                        return render(request, "munters.html", {
                            'date': date_str,
                            'meter_reading': meter_reading,
                        })
                    else : 
                        new_record = MuntersConsumption.objects.create(
                        date=date_obj,
                        meter_reading=meter_reading ,
                        daily_consumption= next_record.meter_reading - meter_reading
                        )
                        redirect_url = reverse('show_munters')
                        return redirect(redirect_url)

                else:
                    new_record = MuntersConsumption.objects.create(
                    date=date_obj,
                    meter_reading=meter_reading ,
                    daily_consumption= 0
                    )
                    redirect_url = reverse('show_munters')
                    return redirect(redirect_url)
    return render(request, "munters.html")

def delete_munters(request, id):
    consumption = get_object_or_404(MuntersConsumption, pk=id)
    previous_row = MuntersConsumption.objects.filter(date__lt=consumption.date).order_by('-date').first()

    if previous_row:
        previous_row.daily_consumption = 0
        previous_row.save()

    consumption.delete()

    redirect_url = reverse('show_munters')
    return redirect(redirect_url)


def add_machine(request):
    if request.method == 'POST':
        # Extraire les données de la requête POST
        nom = request.POST.get('nom')
        panne = request.POST.get('panne')

        # Créer un nouvel objet EnergyConsumption et l'enregistrer dans la base de données
        Machines.objects.create(nom=nom, panne=panne)


        # Construire l'URL de redirection avec les paramètres year et month
        redirect_url = reverse('show_machines') 

        return redirect(redirect_url)

    return render(request, "add_machine.html")
    
### END INSERTION OF RECORDS ###

## EXCEL EXPORT ##

def export_to_excel(data,filename):
    wb = Workbook()
    ws = wb.active
    ws.sheet_view.rightToLeft = True

    ws.append(["Date","Relevé du Compteur","Consommation Journalière"])
    for item in data:
        ws.append([item["date"], item["releve"], item["consommation"]])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachement; filename={filename}.xlsx'
    wb.save(response)
    return response

def export_to_excel_monthly(data,filename):
    wb = Workbook()
    ws = wb.active
    ws.sheet_view.rightToLeft = True

    ws.append(["Mois","Total Consumption","Compteur"])
    for item in data:
        ws.append([item["mois"], item["total_consumption"], item["compteur"]])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachement; filename={filename}.xlsx'
    wb.save(response)
    return response

## END EXCEL EXPORT ##

################################################################  EXPORT WATER  ###########################################################################
@login_required(login_url='login')
def get_water(request):
    water_consumptions = WaterConsumption.objects.all()
    data = []
    for p in water_consumptions:
        data.append({
                'date': p.date,
                'releve': p.meter_reading,
                'consommation': p.daily_consumption,   
            })

    file_name = 'water_consumption'
    return export_to_excel(data, file_name)

@login_required(login_url='login')
def get_water_filtered(request,year,month):
    water_consumptions = WaterConsumption.objects.all()
    water_consumptions = water_consumptions.filter(
            date__year=year,
            date__month=month
        )
    data = []
    for p in water_consumptions:
        data.append({
                'date': p.date,
                'releve': p.meter_reading,
                'consommation': p.daily_consumption,   
            })

    file_name = 'water_consumption_filtered'
    return export_to_excel(data, file_name)

@login_required(login_url='login')
def export_xl_monthly_water(request):
    monthly_data = get_water_monthly_consumption()
    data = []
    for entry in monthly_data:
        data.append({
                'mois': entry['month'].strftime('%B %Y'),
                'total_consumption': entry['total_consumption'],
                'compteur': entry['max_compteur'],
            })

    file_name = 'water_monthly_consumption'
    return export_to_excel_monthly(data, file_name)

@login_required(login_url='login')
def export_monthly_water_f(request,year):
    monthly_data = get_water_monthly_consumption_filtered(year)
    data = []
    for entry in monthly_data:
        data.append({
                'mois': entry['month'].strftime('%B %Y'),
                'total_consumption': entry['total_consumption'],
                'compteur': entry['max_compteur'],
            })

    file_name = 'water_monthly_consumption_f'
    return export_to_excel_monthly(data, file_name)
################################################################  END EXPORT WATER  #######################################################################


################################################################  EXPORT GAS  #############################################################################
@login_required(login_url='login')
def export_xl_gas(request):
    gas_consumptions = GasConsumption.objects.all()
    data = []
    for p in gas_consumptions:
        data.append({
                'date': p.date,
                'releve': p.meter_reading,
                'consommation': p.daily_consumption,   
            })

    file_name = 'gaz_consumption'
    return export_to_excel(data, file_name)

@login_required(login_url='login')
def export_xl_gas_filtered(request,year,month):
    gas_consumptions = GasConsumption.objects.all()
    gas_consumptions = gas_consumptions.filter(
            date__year=year,
            date__month=month
        )
    data = []
    for p in gas_consumptions:
        data.append({
                'date': p.date,
                'releve': p.meter_reading,
                'consommation': p.daily_consumption,   
            })

    file_name = 'gas_consumptions_filtered'
    return export_to_excel(data, file_name)

@login_required(login_url='login')
def export_monthly_gas(request):
    monthly_data = get_gaz_monthly_consumption()
    data = []
    for entry in monthly_data:
        data.append({
                'mois': entry['month'].strftime('%B %Y'),
                'total_consumption': entry['total_consumption'],
                'compteur': entry['max_compteur'],
            })

    file_name = 'water_monthly_consumption'
    return export_to_excel_monthly(data, file_name)


@login_required(login_url='login')
def export_monthly_gas_f(request,year):
    monthly_data = get_gaz_monthly_consumption_filtered(year)
    data = []
    for entry in monthly_data:
        data.append({
                'mois': entry['month'].strftime('%B %Y'),
                'total_consumption': entry['total_consumption'],
                'compteur': entry['max_compteur'],
            })

    file_name = 'gas_monthly_consumption_f'
    return export_to_excel_monthly(data, file_name)
################################################################  END EXPORT GAS  ########################################################################


################################################################  EXPORT ENERGY  #########################################################################
@login_required(login_url='login')
def export_xl_energy(request):
    energy_consumptions = EnergyConsumption.objects.all()
    data = []
    for p in energy_consumptions:
        data.append({
                'date': p.date,
                'releve': p.meter_reading,
                'consommation': p.daily_consumption,   
            })

    file_name = 'energy_consumption'
    return export_to_excel(data, file_name)

@login_required(login_url='login')
def export_xl_energy_filtered(request,year,month):
    energy_consumptions = EnergyConsumption.objects.all()
    energy_consumptions = energy_consumptions.filter(
            date__year=year,
            date__month=month
        )
    data = []
    for p in energy_consumptions:
        data.append({
                'date': p.date,
                'releve': p.meter_reading,
                'consommation': p.daily_consumption,   
            })

    file_name = 'energy_consumptions_filtered'
    return export_to_excel(data, file_name)

@login_required(login_url='login')
def export_monthly_energy(request):
    monthly_data = get_energy_monthly_consumption()
    data = []
    for entry in monthly_data:
        data.append({
                'mois': entry['month'].strftime('%B %Y'),
                'total_consumption': entry['total_consumption'],
                'compteur': entry['max_compteur'],
            })

    file_name = 'energy_monthly_consumption'
    return export_to_excel_monthly(data, file_name)

@login_required(login_url='login')
def export_monthly_energy_f(request,year):
    monthly_data = get_energy_monthly_consumption_filtered(year)
    data = []
    for entry in monthly_data:
        data.append({
                'mois': entry['month'].strftime('%B %Y'),
                'total_consumption': entry['total_consumption'],
                'compteur': entry['max_compteur'],
            })

    file_name = 'energy_monthly_consumption_f'
    return export_to_excel_monthly(data, file_name)
################################################################  END EXPORT ENERGY  #####################################################################


################################################################  EXPORT MUNTERS  #########################################################################
@login_required(login_url='login')
def export_xl_munters(request):
    munters_consumptions = MuntersConsumption.objects.all()
    data = []
    for p in munters_consumptions:
        data.append({
                'date': p.date,
                'releve': p.meter_reading,
                'consommation': p.daily_consumption,   
            })

    file_name = 'munters_consumptions'
    return export_to_excel(data, file_name)

@login_required(login_url='login')
def export_xl_munters_filtered(request,year,month):
    munters_consumptions = MuntersConsumption.objects.all()
    munters_consumptions = munters_consumptions.filter(
            date__year=year,
            date__month=month
        )
    data = []
    for p in munters_consumptions:
        data.append({
                'date': p.date,
                'releve': p.meter_reading,
                'consommation': p.daily_consumption,   
            })

    file_name = 'munters_consumptions_filtered'
    return export_to_excel(data, file_name)

@login_required(login_url='login')
def export_monthly_munters(request):
    monthly_data = get_munters_monthly_consumption()
    data = []
    for entry in monthly_data:
        data.append({
                'mois': entry['month'].strftime('%B %Y'),
                'total_consumption': entry['total_consumption'],
                'compteur': entry['max_compteur'],
            })

    file_name = 'munters_monthly_consumption'
    return export_to_excel_monthly(data, file_name)

@login_required(login_url='login')
def export_monthly_munters_f(request,year):
    monthly_data = get_munters_monthly_consumption_filtered(year)
    data = []
    for entry in monthly_data:
        data.append({
                'mois': entry['month'].strftime('%B %Y'),
                'total_consumption': entry['total_consumption'],
                'compteur': entry['max_compteur'],
            })

    file_name = 'munters_monthly_consumption_f'
    return export_to_excel_monthly(data, file_name)
################################################################  END EXPORT MUNTERS  #####################################################################

def add_water_monthly_consumption(request):
    
     if request.method == 'POST':
        # Extract data from the POST request
        month = request.POST.get('month')
        year = request.POST.get('year')
        prix_u_old = request.POST.get('prix_u_old')
              
        # Obtain the first and last meter readings for the specified month and year
        first_reading = WaterConsumption.objects.filter(date__month=month, date__year=year).aggregate(first_reading=Min('meter_reading'))
        last_reading = WaterConsumption.objects.filter(date__month=month, date__year=year).aggregate(last_reading=Max('meter_reading'))
        
        # Extract the meter readings from the aggregated results
        old_meter = first_reading['first_reading']
        new_meter = last_reading['last_reading']
            
        WaterMonthlyConsumption.objects.create(month=month, year = year,prix_u_old=prix_u_old,old_meter=old_meter,new_meter=new_meter) 
      
        # Create a new WaterConsumption object and save it to the database
        return redirect('show_monthly_water')
        
     return render(request, "eau_monthly_consumption.html")



### ENERGY MONTHLY ###
def get_energy_monthly_consumption():
    monthly_consumption = (EnergyConsumption.objects
                           .annotate(month=TruncMonth('date'))
                           .values('month')
                           .annotate(total_consumption=Sum('daily_consumption'),max_compteur=Max('meter_reading'))
                           .order_by('month'))
    return monthly_consumption

def get_energy_monthly_consumption_filtered(year):
    monthly_consumption = (EnergyConsumption.objects
                           .annotate(month=TruncMonth('date'))
                           .filter(date__year=year)
                           .values('month')
                           .annotate(total_consumption=Sum('daily_consumption'),max_compteur=Max('meter_reading'))
                           .order_by('month'))
    return monthly_consumption

@login_required(login_url='login')
def energy_monthly_consumption(request):
    monthly_data = get_energy_monthly_consumption()
    context = {'monthly_data': monthly_data}

    year = request.GET.get('year')
    
    isfilter = None
    context['isfilter'] = isfilter

    if year:
        monthly_data = get_energy_monthly_consumption_filtered(year)
        context = {'monthly_data': monthly_data}
        isfilter = True
        context['isfilter'] = isfilter
        context['year'] = year

    return render(request, 'energymonthly_consumption.html', context)

def api_energy_monthly(request):
    monthly_data = get_energy_monthly_consumption()
    data = []
    for entry in monthly_data:
        data.append({
                'month': entry['month'].strftime('%B %Y'),
                'total_consumption': entry['total_consumption'],
                'max_compteur': entry['max_compteur'],
            })

    return JsonResponse(data, safe=False)

def api_energy_monthly_filtered(request,year):
    monthly_data = get_energy_monthly_consumption_filtered(year)
    data = []
    for entry in monthly_data:
        data.append({
                'month': entry['month'].strftime('%B %Y'),
                'total_consumption': entry['total_consumption'],
                'max_compteur': entry['max_compteur'],
            })

    return JsonResponse(data, safe=False)

@login_required(login_url='login')
def energy_mconsumption_chart(request):
    return render(request, 'chart_month_energy.html')



### END ENERGY MONTHLY ###



### MUNTERS MONTHLY ###
def get_munters_monthly_consumption():
    monthly_consumption = (MuntersConsumption.objects
                           .annotate(month=TruncMonth('date'))
                           .values('month')
                           .annotate(total_consumption=Sum('daily_consumption'),max_compteur=Max('meter_reading'))
                           .order_by('month'))
    return monthly_consumption

def get_munters_monthly_consumption_filtered(year):
    monthly_consumption = (MuntersConsumption.objects
                           .annotate(month=TruncMonth('date'))
                           .filter(date__year=year)
                           .values('month')
                           .annotate(total_consumption=Sum('daily_consumption'),max_compteur=Max('meter_reading'))
                           .order_by('month'))
    return monthly_consumption

@login_required(login_url='login')
def munters_monthly_consumption(request):
    monthly_data = get_munters_monthly_consumption()
    context = {'monthly_data': monthly_data}

    year = request.GET.get('year')
    
    isfilter = None
    context['isfilter'] = isfilter

    if year:
        monthly_data = get_munters_monthly_consumption_filtered(year)
        context = {'monthly_data': monthly_data}
        isfilter = True
        context['isfilter'] = isfilter
        context['year'] = year

    return render(request, 'munters_monthly_consumption.html', context)

def api_munters_monthly(request):
    monthly_data = get_munters_monthly_consumption()
    data = []
    for entry in monthly_data:
        data.append({
                'month': entry['month'].strftime('%B %Y'),
                'total_consumption': entry['total_consumption'],
                'max_compteur': entry['max_compteur'],
            })

    return JsonResponse(data, safe=False)

def api_munters_monthly_filtered(request,year):
    monthly_data = get_munters_monthly_consumption_filtered(year)
    data = []
    for entry in monthly_data:
        data.append({
                'month': entry['month'].strftime('%B %Y'),
                'total_consumption': entry['total_consumption'],
                'max_compteur': entry['max_compteur'],
            })

    return JsonResponse(data, safe=False)


@login_required(login_url='login')
def munters_consumption_chart(request):
    return render(request, 'chart_munters.html')


@login_required(login_url='login')
def munters_mconsumption_chart(request):
    return render(request, 'chart_month_munters.html')

def monthly_munters_chart(request):
    if request.method == 'POST':
        month = request.POST.get('month')
        year = request.POST.get('year')
        print(month)
        if month is None or year is None:
            return JsonResponse({'error': 'Month and year must be provided in the request.'}, status=400)

        month = int(month)
        year = int(year)

        # Récupérer les données de consommation d'eau pour le mois et l'année spécifiés
        data = MuntersConsumption.objects.filter(date__month=month, date__year=year)

        # Préparer les données pour Chart.js
        labels = [entry.date.day for entry in data]
        daily_consumptions = [entry.daily_consumption for entry in data]

        # Renvoyer les données filtrées en tant que réponse JSON
        return JsonResponse({
            'labels': labels,
            'daily_consumptions': daily_consumptions
        })

    else:
        # Si la méthode de la requête n'est pas POST, renvoyer une réponse JSON avec un message d'erreur
        return JsonResponse({'error': 'POST method is required for this endpoint.'}, status=405)

    return render(request, 'chart_munters.html')

### END MUNTERS MONTHLY ###





### GAZ MONTHLY ###

def get_gaz_monthly_consumption():
    monthly_consumption = (GasConsumption.objects
                           .annotate(month=TruncMonth('date'))
                           .values('month')
                           .annotate(total_consumption=Sum('daily_consumption'),max_compteur=Max('meter_reading'))
                           .order_by('month'))
    return monthly_consumption

def get_gaz_monthly_consumption_filtered(year):
    monthly_consumption = (GasConsumption.objects
                           .annotate(month=TruncMonth('date'))
                           .filter(date__year=year)
                           .values('month')
                           .annotate(total_consumption=Sum('daily_consumption'),max_compteur=Max('meter_reading'))
                           .order_by('month'))
    return monthly_consumption

@login_required(login_url='login')
def gaz_monthly_consumption(request):
    monthly_data = get_gaz_monthly_consumption()
    context = {'monthly_data': monthly_data}

    year = request.GET.get('year')
    
    isfilter = None
    context['isfilter'] = isfilter

    if year:
        monthly_data = get_gaz_monthly_consumption_filtered(year)
        context = {'monthly_data': monthly_data}
        isfilter = True
        context['isfilter'] = isfilter
        context['year'] = year

    return render(request, 'gaz_monthly_consumption.html', context)

def api_gas_monthly(request):
    monthly_data = get_gaz_monthly_consumption()
    data = []
    for entry in monthly_data:
        data.append({
                'month': entry['month'].strftime('%B %Y'),
                'total_consumption': entry['total_consumption'],
                'max_compteur': entry['max_compteur'],
            })

    return JsonResponse(data, safe=False)

def api_gaz_monthly_filtered(request,year):
    monthly_data = get_gaz_monthly_consumption_filtered(year)
    data = []
    for entry in monthly_data:
        data.append({
                'month': entry['month'].strftime('%B %Y'),
                'total_consumption': entry['total_consumption'],
                'max_compteur': entry['max_compteur'],
            })

    return JsonResponse(data, safe=False)

@login_required(login_url='login')
def gas_mconsumption_chart(request):
    return render(request, 'chart_month_gas.html')



### END GAZ MONTHLY ###


### WATER MONTHLY ###

def get_water_monthly_consumption():
    monthly_consumption = (WaterConsumption.objects
                           .annotate(month=TruncMonth('date'))
                           .values('month')
                           .annotate(total_consumption=Sum('daily_consumption'),max_compteur=Max('meter_reading'))
                           .order_by('month'))
    return monthly_consumption

def get_water_monthly_consumption_filtered(year):
    monthly_consumption = (WaterConsumption.objects
                           .annotate(month=TruncMonth('date'))
                           .filter(date__year=year)
                           .values('month')
                           .annotate(total_consumption=Sum('daily_consumption'),max_compteur=Max('meter_reading'))
                           .order_by('month'))
    return monthly_consumption

@login_required(login_url='login')
def water_monthly_consumption(request):
    monthly_data = get_water_monthly_consumption()
    context = {'monthly_data': monthly_data}

    year = request.GET.get('year')
    
    isfilter = None
    context['isfilter'] = isfilter

    if year:
        monthly_data = get_water_monthly_consumptionchart(year)
        context = {'monthly_data': monthly_data}
        isfilter = True
        context['isfilter'] = isfilter
        context['year'] = year

    return render(request, 'water_monthly_consumption.html', context)

def get_water_monthly_consumptionchart(year):
    monthly_consumption = (WaterConsumption.objects
                           .annotate(month=TruncMonth('date'))
                           .filter(date__year=year)
                           .values('month')
                           .annotate(total_consumption=Sum('daily_consumption'),max_compteur=Max('meter_reading'))
                           .order_by('month'))
    return monthly_consumption

def api_water_monthly(request):
    monthly_data = get_water_monthly_consumption()
    data = []
    for entry in monthly_data:
        data.append({
                'month': entry['month'].strftime('%B %Y'),
                'total_consumption': entry['total_consumption'],
                'max_compteur': entry['max_compteur'],
            })
    return JsonResponse(data, safe=False)

def api_water_monthly_filtered(request,year):
    monthly_data = get_water_monthly_consumptionchart(year)
    data = []
    for entry in monthly_data:
        data.append({
                'month': entry['month'].strftime('%B %Y'),
                'total_consumption': entry['total_consumption'],
                'max_compteur': entry['max_compteur'],
            })

    return JsonResponse(data, safe=False)
### END WATER MONTHLY ###




def show_monthly_water(request):
        # Récupérez les paramètres de l'année  du formulaire
        year = request.GET.get('year')
        # Fetch all water consumption data from the database
        water_monthly_consumptions = WaterMonthlyConsumption.objects.all()
        context = {}
        
           # Filtrez les données si l'année et le mois sont spécifiés
        if year:
          water_monthly_consumptions = water_monthly_consumptions.filter(
            year=year,
          )
          context['water_monthly_consumptions'] = water_monthly_consumptions
        
        # Render template with the data
        return render(request, 'display_water_monthly_consumption.html',context)
     







    






@login_required(login_url='login')
def show_water(request):
    context = {}
    water_consumptions = WaterConsumption.objects.all().order_by('date')
    context['water_consumptions'] = water_consumptions

    # Récupérez les paramètres de l'année et du mois du formulaire
    year = request.GET.get('year')
    month = request.GET.get('month')
    isfilter = None
    context['isfilter'] = isfilter

    monthly_consumption = water_consumptions.aggregate(
        total_monthly_consumption=Sum('daily_consumption')
    )['total_monthly_consumption'] or 0
    context['monthly_consumption'] = monthly_consumption
    

    # Filtrez les données si l'année et le mois sont spécifiés
    if year and month:
        water_consumptions = water_consumptions.filter(
            date__year=year,
            date__month=month
        )
        context['water_consumptions'] = water_consumptions
        isfilter = True
        context['isfilter'] = isfilter
        context['year'] = year
        context['month'] = month
        

        # Calculez la consommation mensuelle
        monthly_consumption = water_consumptions.aggregate(
            total_monthly_consumption=Sum('daily_consumption')
        )['total_monthly_consumption'] or 0
        context['monthly_consumption'] = monthly_consumption
        

    # Passez les données filtrées au template
    return render(request, "display_water_consumption.html", context)


### DAILY CHART WATER ###

def water_consumption_chart(request):
    return render(request, 'chart_eau.html')

def monthly_water_chart(request):
    if request.method == 'POST':
        month = request.POST.get('month')
        year = request.POST.get('year')
        print(month)
        if month is None or year is None:
            return JsonResponse({'error': 'Month and year must be provided in the request.'}, status=400)

        month = int(month)
        year = int(year)

        # Récupérer les données de consommation d'eau pour le mois et l'année spécifiés
        data = WaterConsumption.objects.filter(date__month=month, date__year=year).order_by('date')

        # Préparer les données pour Chart.js
        labels = [entry.date.day for entry in data]
        daily_consumptions = [entry.daily_consumption for entry in data]

        # Renvoyer les données filtrées en tant que réponse JSON
        return JsonResponse({
            'labels': labels,
            'daily_consumptions': daily_consumptions
        })

    else:
        # Si la méthode de la requête n'est pas POST, renvoyer une réponse JSON avec un message d'erreur
        return JsonResponse({'error': 'POST method is required for this endpoint.'}, status=405)

    return render(request, 'chart_eau.html')

################## END ##################

### MONTHLY CHART WATER ###
@login_required(login_url='login')
def water_mconsumption_chart(request):
    return render(request, 'chart_month_eau.html')

def water_mconsumptionchart(request):
    if request.method == 'POST':
        year = request.POST.get('year')
        if year is None:
            return JsonResponse({'error': 'year must be provided in the request.'}, status=400)
        year = int(year)

        # Récupérer les données de consommation d'eau pour le mois et l'année spécifiés
        data = get_water_monthly_consumptionchart(year)

        # Préparer les données pour Chart.js
        labels = [entry['month'] for entry in data]
        total_consumption = [entry['total_consumption'] for entry in data]

        # Renvoyer les données filtrées en tant que réponse JSON
        return JsonResponse({
            'labels': labels,
            'total_consumption': total_consumption
        })

    else:
        # Si la méthode de la requête n'est pas POST, renvoyer une réponse JSON avec un message d'erreur
        return JsonResponse({'error': 'POST method is required for this endpoint.'}, status=405)

    return render(request, 'chart_month_eau.html')

################## END ##################



def water_consumption_monthly_chart(request):
    return render(request, 'chart_monthly_eau.html')


def water_anual_compare_chart(request):
      return render(request, 'water_anual_compare_chart.html')

def show_compare_by_years(request):
    # Vérifier si la requête est POST
    if request.method == 'POST':
        # Récupérer les années à partir des données du formulaire
        yearA = request.POST.get('yearA')
        yearB = request.POST.get('yearB')

        # Récupérer les données pour les années spécifiées
        data_yearA = WaterMonthlyConsumption.objects.filter(year=yearA).order_by('month')
        data_yearB = WaterMonthlyConsumption.objects.filter(year=yearB).order_by('month')
        
        # Préparer les données pour le graphique
        months = [data.month for data in data_yearA]  # Assurez-vous que les mois sont dans le bon ordre
        totals_yearA = [data.old_meter for data in data_yearA]
        totals_yearB = [data.new_meter for data in data_yearB]

        context = {
            'yearA': yearA,
            'yearB': yearB,
            'months': months,
            'totals_yearA': totals_yearA,
            'totals_yearB': totals_yearB,
        }
        
        # Retourner le template avec le contexte
        return render(request, 'water_anual_compare_chart.html', context)
    else:
        # Si ce n'est pas une requête POST, rediriger ou afficher une page par défaut
        return render(request, 'water_anual_compare_chart..html')

def get_consumption_data(request):
    if request.method == 'GET':
        year = request.GET.get('year')
        try:
            # Récupérer les données de consommation pour l'année spécifiée depuis la base de données
            consumption_data = WaterMonthlyConsumption.objects.filter(year=year)
            months = []
            total_old = []
            total_new=[]

            # Parcourir les données et extraire les mois et les montants totaux de consommation
            for data in consumption_data:
                months.append(data.month)
                total_old.append(data.old_meter)
                total_new.append(data.new_meter)

            # Retourner les données au format JSON
            return JsonResponse({'months': months, 'total_old': total_old,'total_new': total_new})
        except Exception as e:
            # Gérer les erreurs comme vous le souhaitez, par exemple, renvoyer une réponse d'erreur JSON
            return JsonResponse({'error': str(e)}, status=500)



def show_Energy(request):
    energy_consumptions_query = EnergyConsumption.objects.all().order_by('date')
    context = {}
    context['energy_consumptions'] = energy_consumptions_query


    year = request.GET.get('year')
    month = request.GET.get('month')
    isfilter = None
    context['isfilter'] = isfilter

    monthly_consumption = energy_consumptions_query.aggregate(
            total_monthly_consumption=Sum('daily_consumption')
        )['total_monthly_consumption'] or 0
    context['monthly_consumption'] = monthly_consumption

    if year and month:
        print(year)
        energy_consumptions_query = energy_consumptions_query.filter(
            date__year=year,
            date__month=month
        )
        context['energy_consumptions'] = energy_consumptions_query
        isfilter = True
        context['isfilter'] = isfilter
        context['year'] = year
        context['month'] = month

        # Calculez la consommation mensuelle
        monthly_consumption = energy_consumptions_query.aggregate(
            total_monthly_consumption=Sum('daily_consumption')
        )['total_monthly_consumption'] or 0
        context['monthly_consumption'] = monthly_consumption

    # Rendez le template avec les données
    return render(request, 'display_energy_consumption.html', context)



def add_energy_monthly_consumption(request):
    
     if request.method == 'POST':
        # Extract data from the POST request
        month = request.POST.get('month')
        year = request.POST.get('year')
              
        # Obtain the first and last meter readings for the specified month and year
        first_reading = EnergyConsumption.objects.filter(date__month=month, date__year=year).aggregate(first_reading=Min('meter_reading'))
        last_reading = EnergyConsumption.objects.filter(date__month=month, date__year=year).aggregate(last_reading=Max('meter_reading'))
        
        # Extract the meter readings from the aggregated results
        old_meter = first_reading['first_reading']
        new_meter = last_reading['last_reading']
        prix_u_old = request.POST.get('prix_u_old')
       
        EnergyMonthlyConsumption.objects.create(month=month, year = year,old_meter=old_meter,new_meter=new_meter,prix_u_old=prix_u_old) 
      
        # Create a new WaterConsumption object and save it to the database
        return redirect('show_monthly_energy')
        
     return render(request, "energy_monthly_consumption.html")

def show_monthly_energy(request):
        # Récupérez les paramètres de l'année  du formulaire
        year = request.GET.get('year')
        # Fetch all water consumption data from the database
        energy_monthly_consumptions = EnergyMonthlyConsumption.objects.all()
        context = {}
        
           # Filtrez les données si l'année et le mois sont spécifiés
        if year:
          energy_monthly_consumptions = energy_monthly_consumptions.filter(
            year=year,
          )
          context['energy_monthly_consumptions'] = energy_monthly_consumptions
        
        # Render template with the data
        return render(request, 'display_energy_monthly_consumption.html',context)
     


def energy_consumption_chart(request):
    return render(request, 'chart_energy.html')

def monthly_energy_chart(request):
    if request.method == 'POST':
        month = request.POST.get('month')
        year = request.POST.get('year')
        print(month)
        if month is None or year is None:
            return JsonResponse({'error': 'Month and year must be provided in the request.'}, status=400)

        month = int(month)
        year = int(year)

        # Récupérer les données de consommation d'eau pour le mois et l'année spécifiés
        data = EnergyConsumption.objects.filter(date__month=month, date__year=year).order_by('date')

        # Préparer les données pour Chart.js
        labels = [entry.date.day for entry in data]
        daily_consumptions = [entry.daily_consumption for entry in data]

        # Renvoyer les données filtrées en tant que réponse JSON
        return JsonResponse({
            'labels': labels,
            'daily_consumptions': daily_consumptions
        })

    else:
        # Si la méthode de la requête n'est pas POST, renvoyer une réponse JSON avec un message d'erreur
        return render(request,"chart_energy",JsonResponse({'error': 'POST method is required for this endpoint.'}, status=405))

    return render(request, 'chart_energy.html')

def energy_consumption_monthly_chart(request):
    return render(request, 'chart_monthly_energy.html')


def energy_anual_compare_chart(request):
      return render(request, 'energy_anual_compare_chart.html')

def show_compare_by_years_energy(request):
    # Vérifier si la requête est POST
    if request.method == 'POST':
        # Récupérer les années à partir des données du formulaire
        yearA = request.POST.get('yearA')
        yearB = request.POST.get('yearB')

        # Récupérer les données pour les années spécifiées
        data_yearA = EnergyMonthlyConsumption.objects.filter(year=yearA).order_by('month')
        data_yearB = EnergyMonthlyConsumption.objects.filter(year=yearB).order_by('month')
        
        # Préparer les données pour le graphique
        months = [data.month for data in data_yearA]  # Assurez-vous que les mois sont dans le bon ordre
        totals_yearA = [data.old_meter for data in data_yearA]
        totals_yearB = [data.new_meter for data in data_yearB]

        context = {
            'yearA': yearA,
            'yearB': yearB,
            'months': months,
            'totals_yearA': totals_yearA,
            'totals_yearB': totals_yearB,
        }
        
        # Retourner le template avec le contexte
        return render(request, 'energy_anual_compare_chart.html', context)
    else:
        # Si ce n'est pas une requête POST, rediriger ou afficher une page par défaut
        return render(request, 'energy_anual_compare_chart.html')

def get_consumption_data_energy(request):
    if request.method == 'GET':
        year = request.GET.get('year')
        try:
            # Récupérer les données de consommation pour l'année spécifiée depuis la base de données
            consumption_data = EnergyMonthlyConsumption.objects.filter(year=year)
            months = []
            total_old = []
            total_new=[]

            # Parcourir les données et extraire les mois et les montants totaux de consommation
            for data in consumption_data:
                months.append(data.month)
                total_old.append(data.old_meter)
                total_new.append(data.new_meter)

            # Retourner les données au format JSON
            return JsonResponse({'months': months, 'total_old': total_old,'total_new': total_new})
        except Exception as e:
            # Gérer les erreurs comme vous le souhaitez, par exemple, renvoyer une réponse d'erreur JSON
            return JsonResponse({'error': str(e)}, status=500)

def show_munters(request):
    munters_consumptions = MuntersConsumption.objects.all().order_by('date')
    context = {}
    context['munters_consumptions'] = munters_consumptions

    # Récupérez les paramètres de l'année et du mois du formulaire
    year = request.GET.get('year')
    month = request.GET.get('month')
    isfilter = None
    context['isfilter'] = isfilter

    monthly_consumption = munters_consumptions.aggregate(
            total_monthly_consumption=Sum('daily_consumption')
    )['total_monthly_consumption'] or 0
    context['monthly_consumption'] = monthly_consumption


    # Filtrez les données si l'année et le mois sont spécifiés
    if year and month:
        munters_consumptions = munters_consumptions.filter(
            date__year=year,
            date__month=month
        )
        # Calculez la consommation mensuelle
        context['munters_consumptions'] = munters_consumptions

        isfilter = True
        context['isfilter'] = isfilter
        context['year'] = year
        context['month'] = month

        monthly_consumption = munters_consumptions.aggregate(
            total_monthly_consumption=Sum('daily_consumption')
        )['total_monthly_consumption'] or 0
        context['monthly_consumption'] = monthly_consumption
    # Passez les données filtrées au template
    return render(request, "display_munters_consumption.html", context)
     
def munters(request):
    data = MuntersConsumption.objects.all()
    context = {
        'data': data
    }
    return render(request, 'chart_munters.html', context)



def show_machines(request):
       
    # Fetch all machines  data from the database
    machines = Machines.objects.all()
    # Render template with the data
    return render(request, 'show_machines.html',{'machines': machines})







def add_gas_monthly_consumption(request):
    
     if request.method == 'POST':
        # Extract data from the POST request
        month = request.POST.get('month')
        year = request.POST.get('year')
        # Obtain the first and last meter readings for the specified month and year
        first_reading = GasConsumption.objects.filter(date__month=month, date__year=year).aggregate(first_reading=Min('meter_reading'))
        last_reading = GasConsumption.objects.filter(date__month=month, date__year=year).aggregate(last_reading=Max('meter_reading'))
        
        # Extract the meter readings from the aggregated results
        old_meter = first_reading['first_reading']
        new_meter = last_reading['last_reading']
        prix_u_old = request.POST.get('prix_u_old')
       
        GasMonthlyConsumption.objects.create(month=month, year = year,old_meter=old_meter,new_meter=new_meter,prix_u_old=prix_u_old) 
      
        # Create a new WaterConsumption object and save it to the database
        return redirect('show_monthly_gas')
        
     return render(request, "gas_monthly_consumption.html")


def show_monthly_gas(request):
        # Récupérez les paramètres de l'année  du formulaire
        year = request.GET.get('year')
        # Fetch all water consumption data from the database
        gas_monthly_consumptions = GasMonthlyConsumption.objects.all()
        context = {}
        
           # Filtrez les données si l'année et le mois sont spécifiés
        if year:
          gas_monthly_consumptions = gas_monthly_consumptions.filter(
            year=year,
          )
          context['gas_monthly_consumptions'] = gas_monthly_consumptions
        
        # Render template with the data
        return render(request, 'display_gas_monthly_consumption.html',context)
     


@login_required(login_url='login')
def show_Gas(request):
    gas_consumptions = GasConsumption.objects.all().order_by('date')
    context = {}
    context['gas_consumptions'] = gas_consumptions

    # Récupérez les paramètres de l'année et du mois du formulaire
    year = request.GET.get('year')
    month = request.GET.get('month')
    isfilter = None
    context['isfilter'] = isfilter

    monthly_consumption = gas_consumptions.aggregate(
            total_monthly_consumption=Sum('daily_consumption')
    )['total_monthly_consumption'] or 0
    context['monthly_consumption'] = monthly_consumption


    # Filtrez les données si l'année et le mois sont spécifiés
    if year and month:
        gas_consumptions = gas_consumptions.filter(
            date__year=year,
            date__month=month
        )
        # Calculez la consommation mensuelle
        context['gas_consumptions'] = gas_consumptions

        isfilter = True
        context['isfilter'] = isfilter
        context['year'] = year
        context['month'] = month

        monthly_consumption = gas_consumptions.aggregate(
            total_monthly_consumption=Sum('daily_consumption')
        )['total_monthly_consumption'] or 0
        context['monthly_consumption'] = monthly_consumption
        
    # Passez les données filtrées au template
    return render(request, "display_gas_consumption.html", context)

def  gas_consumption_chart(request):
    return render(request, 'chart_gas.html')

def monthly_gas_chart(request):
    if request.method == 'POST':
        month = request.POST.get('month')
        year = request.POST.get('year')
        print(month)
        if month is None or year is None:
            return JsonResponse({'error': 'Month and year must be provided in the request.'}, status=400)

        month = int(month)
        year = int(year)

        # Récupérer les données de consommation d'eau pour le mois et l'année spécifiés
        data = GasConsumption.objects.filter(date__month=month, date__year=year).order_by('date')

        # Préparer les données pour Chart.js
        labels = [entry.date.day for entry in data]
        daily_consumptions = [entry.daily_consumption for entry in data]

        # Renvoyer les données filtrées en tant que réponse JSON
        return JsonResponse({
            'labels': labels,
            'daily_consumptions': daily_consumptions
        })

    else:
        # Si la méthode de la requête n'est pas POST, renvoyer une réponse JSON avec un message d'erreur
        return render(request,"chart_gas.html",JsonResponse({'error': 'POST method is required for this endpoint.'}, status=405))

    return render(request, 'chart_gas.html')

def gas_consumption_monthly_chart(request):
    return render(request, 'chart_monthly_gas.html')


def get_consumption_data_gas(request):
    if request.method == 'GET':
        year = request.GET.get('year')
        try:
            # Récupérer les données de consommation pour l'année spécifiée depuis la base de données
            consumption_data = GasMonthlyConsumption.objects.filter(year=year)
            months = []
            total_old = []
            total_new=[]

            # Parcourir les données et extraire les mois et les montants totaux de consommation
            for data in consumption_data:
                months.append(data.month)
                total_old.append(data.old_meter)
                total_new.append(data.new_meter)

            # Retourner les données au format JSON
            return JsonResponse({'months': months, 'total_old': total_old,'total_new': total_new})
        except Exception as e:
            # Gérer les erreurs comme vous le souhaitez, par exemple, renvoyer une réponse d'erreur JSON
            return JsonResponse({'error': str(e)}, status=500)


def gas_anual_compare_chart(request):
      return render(request, 'gas_anual_compare_chart.html')

def show_compare_by_years_gas(request):
    # Vérifier si la requête est POST
    if request.method == 'POST':
        # Récupérer les années à partir des données du formulaire
        yearA = request.POST.get('yearA')
        yearB = request.POST.get('yearB')

        # Récupérer les données pour les années spécifiées
        data_yearA = GasMonthlyConsumption.objects.filter(year=yearA).order_by('month')
        data_yearB = GasMonthlyConsumption.objects.filter(year=yearB).order_by('month')
        
        # Préparer les données pour le graphique
        months = [data.month for data in data_yearA]  # Assurez-vous que les mois sont dans le bon ordre
        totals_yearA = [data.old_meter for data in data_yearA]
        totals_yearB = [data.new_meter for data in data_yearB]

        context = {
            'yearA': yearA,
            'yearB': yearB,
            'months': months,
            'totals_yearA': totals_yearA,
            'totals_yearB': totals_yearB,
        }
        
        # Retourner le template avec le contexte
        return render(request, 'gas_anual_compare_chart.html', context)
    else:
        # Si ce n'est pas une requête POST, rediriger ou afficher une page par défaut
        return render(request, 'gas_anual_compare_chart..html')

def get_daily_consumption(request):
    year = int(request.GET.get('year', 2024))
    month = int(request.GET.get('month', 1))

    # Calculer les dates de début et de fin pour le mois donné
    start_date = make_aware(datetime(year, month, 1))
    end_date = make_aware(datetime(year, month + 1, 1)) if month < 12 else make_aware(datetime(year + 1, 1, 1))

    # Filtrer les données pour le mois spécifié
    water_data = list(WaterConsumption.objects.filter(date__range=(start_date, end_date)).values('date', 'daily_consumption'))
    energy_data = list(EnergyConsumption.objects.filter(date__range=(start_date, end_date)).values('date', 'daily_consumption'))
    gas_data = list(GasConsumption.objects.filter(date__range=(start_date, end_date)).values('date', 'daily_consumption'))

    # Préparer les données pour le graphique
    data = {
        'water': water_data,
        'energy': energy_data,
        'gas': gas_data
    }
    return JsonResponse(data)

def modify_water(request, id):
    consumption = get_object_or_404(WaterConsumption, pk=id)
    if request.method == 'POST':
        try:
            # Récupérer les nouvelles valeurs depuis le formulaire
            new_daily_consumption = int(request.POST.get('daily_consumption'))
            new_meter_reading = int(request.POST.get('meter_reading'))

            # Calculer la différence de consommation
            consumption_diff = new_daily_consumption - consumption.daily_consumption

            # Mettre à jour l'enregistrement actuel
            consumption.daily_consumption = new_daily_consumption
            consumption.meter_reading = new_meter_reading
            consumption.save()

   
            # Redirection avec les paramètres year et month
            date_obj = consumption.date
            return redirect(f"{reverse('show_water')}?year={date_obj.year}&month={date_obj.month}")
        except Exception as e:
            # En cas d'erreur, rediriger avec les paramètres year et month
            date_obj = consumption.date
            return redirect(f"{reverse('show_water')}?year={date_obj.year}&month={date_obj.month}")
    else:
        context = {
            'consumption': consumption
        }
        return render(request, 'display_water_consumption.html', context)




def modify_water_monthly(request, id):
    consumption = get_object_or_404(WaterMonthlyConsumption, pk=id)
    if request.method == 'POST':
        try:
            # Récupérer les nouvelles valeurs depuis le formulaire
            new_old_meter_reading = request.POST.get('old_meter')
            new_prix_u_old= request.POST.get('prix_u_old')
            new_new_meter_reading = (request.POST.get('new_meter'))
            month= request.POST.get('month')
            year=request.POST.get('year')
            
 
            # Mettre à jour l'enregistrement actuel
            consumption.old_meter= new_old_meter_reading
            consumption.prix_u_old = new_prix_u_old
            consumption.new_meter= new_new_meter_reading
            consumption.save()
   
            # Redirection avec les paramètres year et month
            return redirect(f"{reverse('show_monthly_water')}?year={year}&month={month}")
        except Exception as e:
            # En cas d'erreur, rediriger avec les paramètres year et month
            month= int(request.POST.get('month'))
            year= int(request.POST.get('year'))
            
            return redirect(f"{reverse('show_monthly_water')}?year={year}&month={month}")
    else:
        context = {
            'consumption': consumption
        }
        return render(request, 'display_water_monthly_consumption.html', context)

def delete_water_monthly(request, id):
    consumption = get_object_or_404(WaterMonthlyConsumption, pk=id)
    month = request.POST.get('month')
    year = request.POST.get('year')

    consumption.delete()

    redirect_url = reverse('show_monthly_water') + f'?year={year}&month={month}'
    return redirect(redirect_url)


def modify_energy(request, id):
    consumption = get_object_or_404(EnergyConsumption, pk=id)
    if request.method == 'POST':
        try:
            # Récupérer les nouvelles valeurs depuis le formulaire
            new_daily_consumption = int(request.POST.get('daily_consumption'))
            new_meter_reading = int(request.POST.get('meter_reading'))

            # Calculer la différence de consommation
            consumption_diff = new_daily_consumption - consumption.daily_consumption

            # Mettre à jour l'enregistrement actuel
            consumption.daily_consumption = new_daily_consumption
            consumption.meter_reading = new_meter_reading
            consumption.save()

   
            # Redirection avec les paramètres year et month
            date_obj = consumption.date
            return redirect(f"{reverse('show_Energy')}?year={date_obj.year}&month={date_obj.month}")
        except Exception as e:
            # En cas d'erreur, rediriger avec les paramètres year et month
            date_obj = consumption.date
            return redirect(f"{reverse('show_Energy')}?year={date_obj.year}&month={date_obj.month}")
    else:
        context = {
            'consumption': consumption
        }
        return render(request, 'display_energy_consumption.html', context)

""" def delete_energy(request, id):
    consumption = get_object_or_404(EnergyConsumption, pk=id)
    consumption_date = request.POST.get('consumption_date')
    date_obj = datetime.strptime(consumption_date, '%Y-%m-%d')
    
    consumption.delete()

    redirect_url = reverse('show_Energy') + f'?year={date_obj.year}&month={date_obj.month}'
    return redirect(redirect_url) """


def modify_energy_monthly(request, id):
    consumption = get_object_or_404(EnergyMonthlyConsumption, pk=id)
    if request.method == 'POST':
        try:
            # Récupérer les nouvelles valeurs depuis le formulaire
            new_old_meter_reading = request.POST.get('old_meter')
            new_prix_u_old= request.POST.get('prix_u_old')
            new_new_meter_reading = (request.POST.get('new_meter'))
            month= request.POST.get('month')
            year=request.POST.get('year')
            
 
            # Mettre à jour l'enregistrement actuel
            consumption.old_meter= new_old_meter_reading
            consumption.prix_u_old = new_prix_u_old
            consumption.new_meter= new_new_meter_reading
            consumption.save()
            print(consumption.old_meter)
            print(consumption.new_meter)
   
            # Redirection avec les paramètres year et month
            return redirect(f"{reverse('show_monthly_energy')}?year={year}&month={month}")
        except Exception as e:
            # En cas d'erreur, rediriger avec les paramètres year et month
            month= int(request.POST.get('month'))
            year= int(request.POST.get('year'))
            
            return redirect(f"{reverse('show_monthly_energy')}?year={year}&month={month}")
    else:
        context = {
            'consumption': consumption
        }
        return render(request, 'display_energy_monthly_consumption.html', context)

def delete_energy_monthly(request, id):
    consumption = get_object_or_404(EnergyMonthlyConsumption, pk=id)
    month = request.POST.get('month')
    year = request.POST.get('year')

    consumption.delete()

    redirect_url = reverse('show_monthly_energy') + f'?year={year}&month={month}'
    return redirect(redirect_url)


def modify_gas(request, id):
    consumption = get_object_or_404(GasConsumption, pk=id)
    if request.method == 'POST':
        try:
            # Récupérer les nouvelles valeurs depuis le formulaire
            new_daily_consumption = int(request.POST.get('daily_consumption'))
            new_meter_reading = int(request.POST.get('meter_reading'))

            # Calculer la différence de consommation
            consumption_diff = new_daily_consumption - consumption.daily_consumption

            # Mettre à jour l'enregistrement actuel
            consumption.daily_consumption = new_daily_consumption
            consumption.meter_reading = new_meter_reading
            consumption.save()

   
            # Redirection avec les paramètres year et month
            date_obj = consumption.date
            return redirect(f"{reverse('show_Gas')}?year={date_obj.year}&month={date_obj.month}")
        except Exception as e:
            # En cas d'erreur, rediriger avec les paramètres year et month
            date_obj = consumption.date
            return redirect(f"{reverse('show_Gas')}?year={date_obj.year}&month={date_obj.month}")
    else:
        context = {
            'consumption': consumption
        }
        return render(request, 'display_gas_consumption.html', context)

""" def delete_gas(request, id):
    consumption = get_object_or_404(GasConsumption, pk=id)
    consumption_date = request.POST.get('consumption_date')
    date_obj = datetime.strptime(consumption_date, '%Y-%m-%d')
    
    consumption.delete()

    redirect_url = reverse('show_Gas') + f'?year={date_obj.year}&month={date_obj.month}'
    return redirect(redirect_url) """


def modify_gas_monthly(request, id):
    consumption = get_object_or_404(GasMonthlyConsumption, pk=id)
    if request.method == 'POST':
        try:
            # Récupérer les nouvelles valeurs depuis le formulaire
            new_old_meter_reading = request.POST.get('old_meter')
            new_prix_u_old= request.POST.get('prix_u_old')
            new_new_meter_reading = (request.POST.get('new_meter'))
            month= request.POST.get('month')
            year=request.POST.get('year')
            
 
            # Mettre à jour l'enregistrement actuel
            consumption.old_meter= new_old_meter_reading
            consumption.prix_u_old = new_prix_u_old
            consumption.new_meter= new_new_meter_reading
            consumption.save()
            print(consumption.old_meter)
            print(consumption.new_meter)
   
            # Redirection avec les paramètres year et month
            return redirect(f"{reverse('show_monthly_gas')}?year={year}&month={month}")
        except Exception as e:
            # En cas d'erreur, rediriger avec les paramètres year et month
            month= int(request.POST.get('month'))
            year= int(request.POST.get('year'))
            
            return redirect(f"{reverse('show_monthly_gas')}?year={year}&month={month}")
    else:
        context = {
            'consumption': consumption
        }
        return render(request, 'display_gas_monthly_consumption.html', context)

def delete_gas_monthly(request, id):
    consumption = get_object_or_404(GasMonthlyConsumption, pk=id)
    month = request.POST.get('month')
    year = request.POST.get('year')

    consumption.delete()

    redirect_url = reverse('show_monthly_gas') + f'?year={year}&month={month}'
    return redirect(redirect_url)

def modify_munters_monthly(request, id):
    consumption = get_object_or_404(Munters, pk=id)
    if request.method == 'POST':
        try:
            # Récupérer les nouvelles valeurs depuis le formulaire
            elec_consumption= (request.POST.get('elec_consumption'))
            munters_consumption = (request.POST.get('munters_consumption'))
            facture_DTTC= (request.POST.get('facture_DTTC'))
            elec_munters_DTTC= (request.POST.get('elec_munters_DTTC')) 
            month= request.POST.get('month')
            year=request.POST.get('year')
            
 
            # Mettre à jour l'enregistrement actuel
            consumption.elec_consumption = elec_consumption
            consumption.munters_consumption= munters_consumption
            consumption.facture_DTTC = facture_DTTC
            consumption.elec_munters_DTTC = elec_munters_DTTC
            consumption.save()
            print(consumption.old_meter)
            print(consumption.new_meter)
   
            # Redirection avec les paramètres year et month
            return redirect(f"{reverse('show_munters_elec')}?year={year}&month={month}")
        except Exception as e:
            # En cas d'erreur, rediriger avec les paramètres year et month
            month= int(request.POST.get('month'))
            year= int(request.POST.get('year'))
            
            return redirect(f"{reverse('show_munters_elec')}?year={year}&month={month}")
    else:
        context = {
            'consumption': consumption
        }
        return render(request, 'display_munters_consumption.html', context)

def delete_munters_monthly(request, id):
    consumption = get_object_or_404(Munters, pk=id)
    month = request.POST.get('month')
    year = request.POST.get('year')

    consumption.delete()

    redirect_url = reverse('show_munters_elec') + f'?year={year}&month={month}'
    return redirect(redirect_url)

