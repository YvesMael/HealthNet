from rest_framework import routers
from django.urls import path
from .views import HospitalDetailAPI, UserDetailAPI, resultat_creation_user, LoginView, LogoutView, liste
# router = routers.DefaultRouter()

urlpatterns = [
    path('Hospital/', HospitalDetailAPI.as_view()),
    path('User/<uidb64>/', UserDetailAPI.as_view()),
    path('validation_email/', resultat_creation_user, name="resultat_creation_user"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('riane/', liste),
    # path('createUser/<uidb64>/', register_user, name="register_user"),
]

