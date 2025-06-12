from django.apps import apps
from django.conf import settings
import time
from openpyxl import Workbook
from .models import Template
import pandas as pd
from io import BytesIO

def getCurrentApps():
    current_apps = apps.get_app_configs()
    field_options = [('','-- Select app --')]
    for app in current_apps:
        #if app.path.startswith(str(settings.BASE_DIR)) and app.name != 'xlsx': # Get only the apps located physically in your project
        if app.path.startswith(str(settings.BASE_DIR)): # Get only the apps located physically in your project
            field_options.append((app.name,app.name))
    return sorted(field_options)

def getCurrentModels():
    field_options = []
    for app in apps.get_app_configs():
        if app.path.startswith(str(settings.BASE_DIR)): # Get only the apps located physically in your project
            app_details = apps.get_app_config(app.name)
            for model in app_details.get_models():
                field_options.append((model.__name__,model._meta.verbose_name))
    return field_options

def getModelsByApp(app):
    app_obj = apps.get_app_config(app)
    models_choices = []    
    for model in app_obj.get_models():
        models_choices.append((model.__name__,model._meta.verbose_name))
    return models_choices

def getColumn(pos=0):
    columns = ['A','B','C','D','E','F','G','H','I','J','K','M','N','L','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    return columns[pos]

def getColumnsChoices():
    columns = ['A','B','C','D','E','F','G','H','I','J','K','M','N','L','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    columnsChoices = [(i,i) for i in columns]
    columnsChoices.insert(0,('','--Select column--'))
    return columnsChoices

def sync_def():
    print('Running...')
    time.sleep(2)
    print('Ending...')
    return True

def prepare_xlsx_export(queryset,template_config,config_id):
    workbook = Workbook() # Create file
    current_sheet = workbook.active # Select sheet    
    
    # Headers
    headers = [template.label for template in template_config]
    current_sheet.append(headers)
    
    # Rows
    for record in queryset:
        row = [str(getattr(record,template.value,'')) for template in template_config]
        current_sheet.append(row)
            
    output = BytesIO()
    workbook.save(output)
    output.seek(0)
    return output