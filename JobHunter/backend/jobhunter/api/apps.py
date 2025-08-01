# api/apps.py
from django.apps import AppConfig
from .utils import load_job_postings

class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        print("ApiConfig.ready() called. Loading data...")
        load_job_postings()  
        print("Data loading complete.")
