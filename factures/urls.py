from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.getall, name="factures"),
    path('addnew/', views.addnew, name="addnewfacture"),
    path('delete/<int:pk>', views.delete_facture, name="delete_facture"),      
]