from celery.result import AsyncResult
from .models import Services, EmployeeWorkInHospital, EmployeeIntervenInService, User, Hospital, Autorisation
from .forms import HospitalSignInForm, ServicesInHospitalForm, RegisterUserForm
from .serializers import HospitalSerializer, ServicesInHospitalSerializer, RegisterUserSerializer
from .tasks import send_email_verification, test_task
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
import json
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from django.db import transaction
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response

@api_view(['POST'])
@parser_classes([MultiPartParser])  # ce decorateur permet de specifier a DRF qu'on recevra des donnees de type multipart/form-data i.e des donnees qui sont envoyees depuis un FormData JavaScript et contenant des images(multipart)
def create_hospital(request):
    hospital_logo = request.FILES.get('logo')
    hospital_data_json = request.data.get('hospital')
    services_data_json = request.data.get('services')

    try:
        hospital_data = json.loads(hospital_data_json)
        services_data = json.loads(services_data_json)
    except json.JSONDecodeError:
        return JsonResponse({'etat': False, 'message': 'Invalid JSON format'}, status=400)

    hospital_instance = HospitalSerializer(data=hospital_data)
    if not hospital_instance.is_valid(raise_exception=True):
        return JsonResponse({'etat': False, 'message': 'Invalid hospital data', 'errors': hospital_instance.errors}, status=400)

    hospital = hospital_instance.save()
    hospital.logo = hospital_logo
    hospital.save()

    service_names = [service.get('name') for service in services_data]
    existing_services = Services.objects.filter(name__in=service_names)
    service_dict = {service.name: service for service in existing_services} # ici nous creons un dictionnaire service_dict = {nom_service1:objet_service, nom_service2:objet_service}
    #Nous aurons donc les noms des services comme cles et les objets services comme valeurs

    for valeur in services_data:
        service = service_dict.get(valeur.get('name'))
        if not service:
            continue  # Dans le cas ou il y'aurait un service dans la liste recuperee qui ne soit pas dans la BD

        service_form_data = {
            'number_of_beds': valeur.get('number_of_beds'),
            'phone_number': valeur.get('phone_number'),
            'email': valeur.get('email')
        }
        service_form = ServicesInHospitalSerializer(data=service_form_data)
        if service_form.is_valid(raise_exception=True):
            service_form.save(id_Hospital=hospital, id_Service=service)

    hospital_id_encoded = urlsafe_base64_encode(force_bytes(hospital.id))
    return JsonResponse({'etat': True, 'message': hospital_id_encoded})


def AccessHospital(request,id_hospital):
    return EmployeeWorkInHospital.objects.filter(id_Hospital = id_hospital , id_Employee = request.user.id ,is_active = True).exists()

def AccessServices(request,id_hospital ,id_service):
    return EmployeeIntervenInService.objects.filter(id_Hospital = id_hospital , id_Employee = request.user.id ,status = True, id_Service = id_service).exists()

@transaction.atomic
@api_view(['POST'])
def register_user(request, uidb64):
    id_hospital = urlsafe_base64_decode(uidb64)
    id_hospital = id_hospital.decode('utf-8')
    donnees = request.POST.get('username')
    the_user_name = donnees.strip()
    try:
        already_Exist = User.objects.get(username=the_user_name)
    except(ValueError, User.DoesNotExist):
        already_Exist = None
    if already_Exist is None:
        # the_password = 'pourquoiTUn@p@sM@ngE@#Weer'
        the_new_user = {
            'username':the_user_name,
            'first_name':request.POST.get('first_name'),
            'last_name':request.POST.get('last_name'),
            'date_of_birth':request.POST.get('date_of_birth'),
            'sex':request.POST.get('sex'),
            'religion':request.POST.get('religion'),
            'occupation':request.POST.get('occupation'),
            'numero_carte_biometrique':request.POST.get('numero_carte_biometrique'),
            'city':request.POST.get('city'),
            'quarter':request.POST.get('quarter'),
            'blood_group':request.POST.get('blood_group'),
            'allergy':request.POST.get('allergy'),
            'phone_number':request.POST.get('phone_number'),
            'email':request.POST.get('email'),
            'marital_status':request.POST.get('marital_status'),
            'nationality':request.POST.get('nationality'),
            'password':request.POST.get('password'),
            'password2':request.POST.get('password2'),
            'created_at':id_hospital
        } 
        serializerUser = RegisterUserSerializer(data=the_new_user)
        if serializerUser.is_valid(raise_exception=True):
            # user_email = serializerUser
            if the_new_user['email'] is not None:
                utilisateur = serializerUser.save(is_active=False)
                domain = get_current_site(request).domain
                tache = test_task.delay()
                return Response({'task_id':tache.id})
            serializerUser.save()
            return Response({'etat':True,'message':'Sauvegarde Reussie mais sans email'})  
        else:
            return Response({'etat':False,'message':'The account form is not valid'})
    else:
        return Response({'etat':False,'message':'change username'})

# cette API nous permet de tester la fin de la tache d'envoie du mail de verification de l'adresse mail
@api_view(['GET'])
def resultat_creation_user(request):
    resultat = AsyncResult(request.GET.get('id_tache'))
    if resultat.state == "SUCCESS":
        data = resultat.result
        if isinstance(data, dict) and 'token' in data and 'uid' in data:
            return Response({'state':resultat.state, 'token':resultat.result['token'], 'uid':resultat.result['uid']})
        return Response({'state':resultat.state,'message':resultat.result})
    else:
        return Response({'state':resultat.state, 'result':None, 'error':str(resultat.result)})

@api_view(['GET'])
def liste(request):
    donnees = Hospital.objects.all()
    serialiser = HospitalSerializer(donnees, many=True)
    return Response(serialiser.data)



