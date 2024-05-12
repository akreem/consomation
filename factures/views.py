from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Facture
from .forms import FactureForm

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

def delete_facture(request,pk):
    f = Facture.objects.get(pk=pk)
    f.delete()
    return HttpResponseRedirect('/factures/')


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

def generate_invoice(request, pk):
    facture = Facture.objects.get(pk=pk)
    # Logic to calculate invoice based on consumption and utility type
    return render(request, 'invoice.html', {'facture': facture})