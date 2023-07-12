from django.urls import path
from . import views

urlpatterns = [ 
    path("", views.roteirosView, name="roteiros-view"),
    path("newroteiro", views.newRoteiroView, name="newroteiro-view"),
    path("roteiro/<int:id>", views.roteirosIdView, name="roteiro-id-view"),
    path("delete/<int:id>", views.deleteRoteiro, name="delete-roteiro"),
    path("edit/<int:id>", views.editRoteiro, name="edit-roteiro")

]
