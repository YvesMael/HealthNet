from celery import shared_task
from django.core.mail import send_mail
from .models import Autorisation, VerificationCode, User, Hospital
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.encoding import force_bytes
from django.conf import settings

@shared_task
def send_email_verification(user_id, domain, id_hospital, password=False): # Ici password me permet de differencier le cas ou la tache est appelee pour une creation de compte du cas ou elle est appelee pour forget_password
    user = User.objects.get(id=user_id)
    hospital = Hospital.objects.get(id=id_hospital)
    Autorisation.objects.create(id_Person=user, id_Hospital=hospital)
    verification = VerificationCode.objects.create(user=user)
    user_email = user.email
    # site = get_current_site(request)
    print("execution de la tache")
    generator = PasswordResetTokenGenerator()
    token_generated = generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.id))
    html_message = render_to_string(template_name='utilisateurs/send_email.html',context={'domain':domain, 'uid':uid, 'token':token_generated, 'user':user,'verification_code':verification.code})
    text_content = strip_tags(html_message)
    
    if password: # Si password est True ca veut dire qu'on l'a appelee depuis la vue de forgot_password
        send_mail(f'Message from Gypsum Company by HealthNet',text_content,settings.EMAIL_HOST_USER,[user_email],fail_silently=False)
    else:
        send_mail(f'Message from Gypsum Company by HealthNet',text_content,settings.EMAIL_HOST_USER,[user_email],fail_silently=False)
    return {'token':token_generated, 'uid':uid}

@shared_task
def test_task():
    return "ok"