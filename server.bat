@echo off
cd C:\Users\Win7
start project_magang\Scripts\activate ^& cd C:\Users\Win7\Documents\dikantorpos ^& start python manage.py runserver 0.0.0.0:8000 --settings=dikantorpos.settings ^& exit