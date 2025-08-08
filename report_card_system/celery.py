import os
from celery import Celery

# Set default settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "report_card_system.settings")

app = Celery("report_card_system")

app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from all registered Django app configs
app.autodiscover_tasks()
