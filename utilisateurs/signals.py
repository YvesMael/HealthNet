from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Services
from django.conf import settings
from django.core.files import File
import os

@receiver(post_migrate)
def create_default_services(sender, **kwargs):
    services = [
        {"name": "Consultation", "icon": "consultation.svg"},
        {"name": "Reception", "icon": "reception-desk.svg"},
        {"name": "Administration", "icon": "opthalmology.svg"},
    ]
    for s in services:
        obj, created = Services.objects.get_or_create(name=s["name"])
        if created and s.get("icon"):
            icon_path = os.path.join(settings.MEDIA_ROOT, 'Images/Icons/', s["icon"])
            with open(icon_path, 'rb') as f:
                obj.icon.save(s["icon"], File(f), save=True)

