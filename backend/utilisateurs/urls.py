from rest_framework import routers
from django.urls import path
from .views import create_hospital, liste, register_user, resultat_creation_user
# router = routers.DefaultRouter()

urlpatterns = [
    path('createHospital/', create_hospital, name='create_hospital'),
    path('liste/', liste),
    path('createUser/<uidb64>/', register_user, name="register_user"),
    path('validation_email/', resultat_creation_user, name="resultat_creation_user"),
]

