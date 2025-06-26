from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from .models import Configuration, Template, TemplateType, FileLogs
from django.apps import apps
from .utils import getColumn
import os
from pathlib import Path

@receiver(post_save, sender=Configuration)
def createTemplateConfig(sender, instance, created, raw, using, **kwargs):
    model = apps.get_model(instance.app,instance.model)
    model_fields = model._meta.get_fields()
    template_types = ['export','import']
    if created:
        for type in template_types:
            for i,v in enumerate(model_fields):
                Template(
                    configuration = instance,
                    type = TemplateType.type_export if type == 'export' else TemplateType.type_import,
                    label = v.name,
                    column = getColumn(i),
                    value = v.name,
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