from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Facture, ProcessClass
from .forms import FactureForm, ProcessForm
from django.shortcuts import  get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def getall(request):
    factures = Facture.objects.all().order_by('-annee', 'mois').values()
    # Récupérez les paramètres de l'année et du mois du formulaire
    month_names = {
        1: 'Janvier', 2: 'Février', 3: 'Mars', 4: 'Avril',
        5: 'Mai', 6: 'Juin', 7: 'Juillet', 8: 'Aout',
        9: 'Septembre', 10: 'Octobre', 11: 'Novembre', 12: 'Décembre'
    }

    factures_with_month_names = []
    for facture in factures:
        facture_with_display = facture.copy()
        facture_with_display['mois_display'] = month_names.get(facture['mois'])
        factures_with_month_names.append(facture_with_display)

    context = {}
    context['factures'] = factures_with_month_names


    year = request.GET.get('year')
    utility_type = request.GET.get('utility_type')

    
    isfilter = None
    context['isfilter'] = isfilter
    #context['factures'] = factures
     # Filtrez les données si l'année et le mois sont spécifiés
    if year and utility_type:
        factures = factures.filter(
            annee=year,
            utility_type=utility_type
        )
        factures_with_month_names1 = []
        for facture in factures:
            facture_with_display = facture.copy()
            facture_with_display['mois_display'] = month_names.get(facture['mois'])
            factures_with_month_names1.append(facture_with_display)

        isfilter = True
        context['isfilter'] = isfilter
        #context['factures'] = factures
        context['factures'] = factures_with_month_names1

    return render(request, 'factures.html', context)

@login_required(login_url='login')
def addnew(request):
    if request.method == 'POST':
        form = FactureForm(request.POST)
        if form.is_valid():
            form.save()
            #return HttpResponseRedirect('generate_invoice', pk=form.instance.pk)
            return HttpResponseRedirect('/factures/')

    else:
        form = FactureForm()
    return render(request, 'create_facture.html', {'form': form})

@login_required(login_url='login')
def delete_facture(request,pk):
    f = Facture.objects.get(pk=pk)
    f.delete()
    return HttpResponseRedirect('/factures/')

@login_required(login_url='login')
def update_facture(request, id):
    factures = get_object_or_404(Facture, pk=id)
    if request.method == 'POST':
        try:
            # Récupérer les nouvelles valeurs depuis le formulaire
            new_consommation = float(request.POST.get('consommationID').replace(',', '.'))
            new_pu = float(request.POST.get('puID').replace(',', '.'))
            new_montant = float(request.POST.get('montantID').replace(',', '.'))
            

            # Mettre à jour l'enregistrement actuel
            factures.consumption = new_consommation
            factures.pu = new_pu
            factures.montant = new_montant
            factures.save()

   
            return redirect(f"{reverse('factures')}")
        except Exception as e:
            # En cas d'erreur, rediriger avec les paramètres year et month

            return redirect("/factures/")

@login_required(login_url='login')
def add_process(request):
    if request.method == 'POST':
        form = ProcessForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            #return HttpResponseRedirect('generate_invoice', pk=form.instance.pk)
            return HttpResponseRedirect('/process')

    else:
        form = ProcessForm()
    return render(request, 'create_process.html', {'form': form})

@login_required(login_url='login')
def get_process(request):
    process = ProcessClass.objects.all()
    return render(request, 'process.html', {'process': process})

@login_required(login_url='login')
def delete_process(request,pk):
    p = ProcessClass.objects.get(pk=pk)
    p.delete()
    return HttpResponseRedirect('/process/')



@login_required(login_url='login')
def generate_invoice(request, pk):
    facture = Facture.objects.get(pk=pk)
    # Logic to calculate invoice based on consumption and utility type
    return render(request, 'invoice.html', {'facture': facture})