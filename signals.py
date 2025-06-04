from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Configuration, Template, TemplateType
from django.apps import apps
from .utils import getColumn

@receiver(post_save, sender=Configuration)
def createTemplateConfig(sender, instance, raw, using, update_fields, **kwargs):

    print('Creando template')
    model = apps.get_model(instance.app,instance.model)
    model_fields = model._meta.get_fields()
    template_types = ['export','import']
    for type in template_types:
        for i,v in enumerate(model_fields):
            Template(
                configuration = instance,
                type = TemplateType.type_export if type == 'export' else TemplateType.type_import,
                label = v.name,
                column = getColumn(i),
                value = v.name,
            ).save()