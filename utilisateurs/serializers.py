from .models import Hospital, ServicesInHospital, User
from rest_framework import serializers
from django.contrib.auth import get_user_model

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ('name','email','location')

class ServicesInHospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicesInHospital
        fields = ('number_of_beds','phone_number','email')

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['username','first_name','last_name','sex','date_of_birth','created_at','email','phone_number','religion','blood_group','city','occupation','numero_carte_biometrique','quarter','allergy','marital_status','nationality','password','password2']

    def validate(self, data):
        if data['password']!=data['password2']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            date_of_birth=validated_data.get('date_of_birth'),
            sex=validated_data.get('sex'),
            created_at=validated_data.get('created_at'),
            phone_number=validated_data.get('phone_number'),
            religion=validated_data.get('religion'),
            blood_group=validated_data.get('blood_group'),
            city=validated_data.get('city'),
            occupation=validated_data.get('occupation'),
            numero_carte_biometrique=validated_data.get('numero_carte_biometrique'),
            quarter=validated_data.get('quarter'),
            allergy=validated_data.get('allergy'),
            marital_status=validated_data.get('marital_status'),
            nationality=validated_data.get('nationality'),
        )
        return user
