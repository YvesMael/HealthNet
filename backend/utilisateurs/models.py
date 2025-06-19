from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import  now, datetime
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from simple_history.models import HistoricalRecords
from PIL import Image
from django.utils.crypto import get_random_string
import random, string


class Services(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    icon = models.FileField(upload_to='Images/Icons/')

class Hospital(models.Model):
    name = models.CharField(max_length=50)
    phone_number = PhoneNumberField()
    email = models.EmailField(blank=True, null=True)
    location = models.CharField(max_length=30)
    logo = models.ImageField(upload_to='Images/', default='Images/defaultlogohospital.jpeg')
    
    IMAGE_MAX_SIZE = (400, 400)

    def resize_image(self):
        image = Image.open(self.logo)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.logo.path)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()

class ServicesInHospital(models.Model):
    id_Hospital = models.ForeignKey(Hospital, on_delete=models.PROTECT, related_name='services')
    id_Service = models.ForeignKey(Services, on_delete=models.PROTECT)
    date_added = models.DateTimeField(auto_now_add=True)
    phone_number = PhoneNumberField(blank=True)
    email = models.EmailField(blank=True, null=True)
    number_of_beds = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords(excluded_fields=['phone_number','email','number_of_beds'])

    class Meta:
        unique_together = ('id_Hospital','id_Service')


class Nationality(models.Model):
    name = models.CharField(max_length=30, primary_key=True)

# L'hopital dans lequel le compte du patient est cree a automatiquement l'autorisation d'acceder a son compte
class User(AbstractUser):

    SEXES = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    )

    MARITAL_STATUS = (
        ('MARRIED', 'Married'),
        ('SINGLE', 'Single'),
    )
    RELIGION = (
        ('CHRISTIAN', 'Christian'),
        ('MUSLIM', 'Muslim'),
        ('ANEMIST', 'Anemist '),
        ('BUDDHIST', 'Buddhist'),
        ('JUDAIST', 'Judaist'),
        ('HINDUS', 'Hindus'),
        ('NOTHING', 'Nothing'),
    )
    BLOOD_GROUPS = (
        ('A', 'A'),
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B', 'B'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB', 'AB'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O', 'O'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    )
    # numero_cni = models.CharField(max_length=50, unique=True)     # Pas besoin d'avoir le numero de CNI ou de carte biometrique pour identifier une personne. On peut le faire avec son Username, son numero de telephone ou son email
    numero_carte_biometrique = models.CharField(max_length=50, blank=True)
    sex = models.CharField(max_length=10, choices=SEXES, blank=True)
    date_of_birth = models.DateField(validators=[MaxValueValidator(now().date())], blank=True, null=True)
    city = models.CharField(max_length=30, blank=True)
    quarter = models.CharField(max_length=50, blank=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS, blank=True)
    blood_group = models.CharField(max_length=4, choices=BLOOD_GROUPS, blank=True)
    religion = models.CharField(max_length=15, choices=RELIGION, blank=True)
    occupation = models.CharField(max_length=50, blank=True)
    allergy = models.CharField(max_length=30, blank=True)
    nationality = models.CharField(max_length=150)
    profil = models.ImageField(upload_to='Images/', default='Images/defaultprofil.jpeg')
    onseat = models.BooleanField(default = True)
    follow = models.ManyToManyField(
        'self',
        through='PersonFollowPerson',
        symmetrical=False,
    )
    created_at = models.ForeignKey(Hospital, on_delete=models.PROTECT, related_name='users', blank=True, null=True)
    history = HistoricalRecords(excluded_fields= ['date_of_birth', 'sex','marital_status','blood_group','denomination','first_name','last_name','password','created_at','is_staff','is_active','onseat'])

    @property
    def age(self):
        aujourdhui = datetime.today().date()
        age_en_jours = (aujourdhui - self.date_of_birth).days
        age_en_mois = age_en_jours // 30
        age_en_annees = age_en_mois // 12

        if age_en_jours < 30:
            return f"{age_en_jours} jours"
        elif age_en_mois < 24:
            return f"{age_en_mois} mois"
        else:
            return f"{age_en_annees} ans"  
        
    IMAGE_MAX_SIZE = (400, 400)
    
    def resize_image(self):
        image = Image.open(self.profil)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.profil.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()


class Specialisation(models.Model):    # Les specialisations possibles doivent etre ajoutees dans l'interface d'administration
    name = models.CharField(max_length=30, primary_key=True)

class VerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='codes')
    code = models.CharField(max_length=10)
    
    def generate_code(self):
        random.seed()
        return get_random_string(length=9, allowed_chars=string.ascii_letters + string.digits)
    
    def save(self, *args, **kwargs):
        self.code = self.generate_code() 
        super().save(*args, **kwargs)

class Autorisation(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    id_Person = models.ForeignKey(User, on_delete=models.PROTECT, related_name='autorisations')
    id_Hospital = models.ForeignKey(Hospital, on_delete=models.PROTECT, related_name='autorisations')

class PersonFollowPerson(models.Model):
    id_Followed = models.ForeignKey(User, on_delete=models.PROTECT, related_name='followed')
    id_Follower = models.ForeignKey(User, on_delete=models.PROTECT, related_name='follower')
    start_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    relationship = models.CharField(max_length=20)
    consent = models.FileField(upload_to='Uploads/', blank=True, null=True)

class EmployeeWorkInHospital(models.Model):
    id_Hospital = models.ForeignKey(Hospital, on_delete=models.PROTECT)
    id_Employee = models.ForeignKey(User, on_delete=models.PROTECT)
    specialisation = models.ForeignKey(Specialisation, on_delete=models.PROTECT, related_name='persons')
    start_date = models.DateField(validators=[MaxValueValidator(now().date())])
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)   # ce champ nous permet de donner la possibilite de retirer le droit a un employe a un moment donne de se connecter en tant que employe de l'hopital (mise a pied)
    history = HistoricalRecords()

    class Meta:
        unique_together = ('id_Hospital', 'id_Employee', 'start_date')

    def clean(self, *args, **kwargs):
        super().clean()
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError("La date de fin doit etre superieur à celle de debut")


class EmployeeIntervenInService(models.Model):
    id_Hospital = models.ForeignKey(Hospital, on_delete=models.PROTECT)
    id_Service = models.ForeignKey(Services, on_delete=models.PROTECT)
    id_Employee = models.ForeignKey(User, on_delete=models.PROTECT)
    date = models.DateTimeField(default=now, validators=[MaxValueValidator(now)])
    chief = models.BooleanField(default=False)
    status = models.BooleanField(default=True)  # qui permet de gerer le cas ou on pourra a un moment donné retirer les droits a un personnel, il nous faudra tout simplement passer status a false
    history = HistoricalRecords()

    class Meta:
        unique_together = ('id_Hospital', 'id_Employee', 'id_Service', 'date')


