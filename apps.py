from django.apps import AppConfig


class XlsxConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'xlsx'
    
    def ready(self):
        from .signals import createTemplateConfig
