from django.apps import AppConfig


class SalesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sales'

    # calculate total sum of sales on signal.
    def ready(self):
        import sales.signals