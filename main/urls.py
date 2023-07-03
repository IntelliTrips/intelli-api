from django.urls import path
from . import views

urlpatterns = [ 
    path("", views.roteiro, name="index")
]
