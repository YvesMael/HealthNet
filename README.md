# HealthNet
Amelioration du projet de gestion et d'interconnexion des hôpitaux. 
#### Utilisation d'une approche plus modulaire et d'API (DRF + ReactJS) + Surveillance réseau avec un SIEM

Pour le faire tourner sur votre PC, il faudra:
  - Installer python (3.12.2)
  - cloner le projet se trouvant sur la branche principale
  - creer un environnement virtuel (python -m venv non_environnement) et l'activer "cd nom_env/Scripts/ && activate" (sur windows :) )
  - installer les dependances du projet (pip install -r requirements.txt)
  - lancer un serveur Web, un moteur de Script et un Serveur de BD (WampServer), y creer la BD "HospitalDataBase"
  - reperer le fichier manage.py et en etant dans le repertoire de ce fichier, taper:
    - #### python manage.py makemigrations
    - #### python manage.py migrate
    - #### python manage.py runserver
  #### Pour faire fonctionner les taches programmées en arrière plan
  - Telecharger Redis-with-services, dézipper et lancer le fichier redis-server dans un CMD (start redis-server)
  - dans un autre terminal taper celery -A backend worker -l info -P gevent

<**> ça y est :)
