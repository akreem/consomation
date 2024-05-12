from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Facture
from .forms import FactureForm
from django.shortcuts import  get_object_or_404
from django.urls import reverse

# Create your views here.
def getall(request):
    factures = Facture.objects.all()
    # Récupérez les paramètres de l'année et du mois du formulaire
    year = request.GET.get('year')
    month = request.GET.get('month')
     # Filtrez les données si l'année et le mois sont spécifiés
    if year and month:
        factures = factures.filter(
            annee=year,
            mois=month
        )

    return render(request, 'factures.html', {'factures': factures})


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

def delete_facture(request,pk):
    f = Facture.objects.get(pk=pk)
    f.delete()
    return HttpResponseRedirect('/factures/')

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

   
            # Redirection avec les paramètres year et month
            date_obj = factures.date
            return redirect(f"{reverse('factures')}?date={date_obj}")
        except Exception as e:
            # En cas d'erreur, rediriger avec les paramètres year et month

            return redirect("/factures/")


def generate_invoice(request, pk):
    facture = Facture.objects.get(pk=pk)
    # Logic to calculate invoice based on consumption and utility type
    return render(request, 'invoice.html', {'facture': facture})