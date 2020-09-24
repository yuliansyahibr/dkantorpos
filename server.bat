@echo off
cd C:\Users\User\Desktop\dkantorpos
start workon project_magang ^& start python manage.py runserver 0.0.0.0:8000 --settings=dikantorpos.settings ^& exit
