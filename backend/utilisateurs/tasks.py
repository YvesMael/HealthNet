from celery import shared_task
# from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from .models import Autorisation, VerificationCode, User
# from .forms import RegisterUserForm
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.encoding import force_bytes
from django.conf import settings

@shared_task
def send_email_verification():
    # user = User.objects.get(id=user_id)
    # Autorisation.objects.create(id_Person=user.id, id_Hospital=id_hospital)
    # verification = VerificationCode.objects.create(user=user)
    # user_email = user.email
    # # site = get_current_site(request)
    # print("execution de la tache")
    # generator = PasswordResetTokenGenerator()
    # token_generated = generator.make_token(user)
    # uid = urlsafe_base64_encode(force_bytes(user.id))
    # html_message = render_to_string('utilisateurs/send_email.html',{'domain':domain, 'uid':uid, 'token':token_generated, 'user':user,'verification_code':verification.code})
    # text_content = strip_tags(html_message)
    # print("envoie du mail")
    send_mail(f'Message from Gypsum Company by HealthNet',"Bonjour",settings.EMAIL_HOST_USER,["yvesmaelt@gmail.com"],fail_silently=False)
    return {'token':'token_generated', 'uid':'uid'}

@shared_task
def test_task():
    return "ok"