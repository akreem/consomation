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