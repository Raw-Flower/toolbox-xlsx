from django.apps import apps
from django.conf import settings

def getCurrentApps():
    current_apps = apps.get_app_configs()
    field_options = [('','-- Select app --')]
    for app in current_apps:
        if app.path.startswith(str(settings.BASE_DIR)): # Get only the apps located physically in your project
            field_options.append((app.name,app.name))
    return sorted(field_options)

def getModelsByApp(app):
    app_obj = apps.get_app_config(app)
    models_choices = []    
    for model in app_obj.get_models():
        models_choices.append((model.__name__,model._meta.verbose_name))
    return models_choices
    