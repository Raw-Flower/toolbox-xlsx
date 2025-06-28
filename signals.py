from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.conf import settings
from .models import Configuration, Template, TemplateType, FileLogs, Configuration
from django.apps import apps
from .utils import getColumn
import os
from pathlib import Path

@receiver(post_save, sender=Configuration)
def createTemplateConfig(sender, instance, created, raw, using, **kwargs):
    if created:
        model = apps.get_model(instance.app,instance.model)
        model_fields = [field.name for field in model._meta.get_fields() if ((field.concrete) and (field.name!='id'))]  
        template_types = ['export','import']
        for type in template_types:
            for i,v in enumerate(model_fields):
                Template(
                    configuration = instance,
                    type = TemplateType.type_export if type == 'export' else TemplateType.type_import,
                    label = v,
                    column = getColumn(i),
                    value = v,
                ).save()
            
@receiver(post_delete, sender=FileLogs)
def removeLogFile(sender, instance, using, origin, **kwargs):
    file_path = Path(f'{settings.BASE_DIR}/{instance.file.url}')
    try:
        os.remove(file_path)
    except FileNotFoundError:
        print(f'ERROR: Image not found in ({file_path}).')  
    except Exception as e:
        print(f'ERROR({type(e).__name__}): {e}')
        
@receiver(post_delete, sender=Configuration)
def removeLogFile(sender, instance, using, origin, **kwargs):
    if instance.import_template:
        file_path = Path(f'{settings.BASE_DIR}/{instance.import_template.url}')
        try:
            os.remove(file_path)
        except FileNotFoundError:
            print(f'ERROR: Image not found in ({file_path}).')  
        except Exception as e:
            print(f'ERROR({type(e).__name__}): {e}')