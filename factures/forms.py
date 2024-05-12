from django import forms
from .models import Facture

class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ['utility_type','typecompteur_eau','date','mois','annee','consumption','pu','cos','montant']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super(FactureForm, self).__init__(*args, **kwargs)
        # Applying CSS classes to the fields        
        self.fields['utility_type'].widget.attrs.update({'class': 'form-control', 'placeholder':'Prenom', 'autofocus': 'autofocus'})
        self.fields['utility_type'].label = "Utilitaire"
        self.fields['typecompteur_eau'].widget.attrs.update({'class': 'form-control', 'placeholder':'Nom'})
        self.fields['typecompteur_eau'].label = "Type de compteur d'eau "
        self.fields['date'].widget.attrs.update({'class': 'form-control'})

        self.fields['mois'].widget.attrs.update({'class': 'form-control', 'placeholder':'Mois'})
        self.fields['mois'].label = "Mois"
        self.fields['annee'].widget.attrs.update({'class': 'form-control', 'placeholder':'Année'})
        self.fields['annee'].label = "Année"
        self.fields['consumption'].widget.attrs.update({'class': 'form-control', 'placeholder':'Consomation'})
        self.fields['consumption'].label = "Consomation"
        self.fields['pu'].widget.attrs.update({'class': 'form-control', 'placeholder':'Prix Unitaire'})
        self.fields['pu'].label = "Prix Unitaire"

        self.fields['cos'].widget.attrs.update({'class': 'form-control', 'placeholder':'Cos Q'})
        self.fields['cos'].label = "Cos Q"

        self.fields['montant'].widget.attrs.update({'class': 'form-control', 'placeholder':'Montant'})
