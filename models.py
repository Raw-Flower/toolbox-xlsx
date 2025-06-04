from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxLengthValidator, MinLengthValidator, RegexValidator, MinValueValidator

# Create your models here.
class Status(models.IntegerChoices):
    enable = (1,'Active')
    disable = (0,'Inactive')
    __empty__ = ('-- Status --')

class TemplateType(models.IntegerChoices):
    type_export = (1,'Export')
    type_import = (2,'Import')
    __empty__ = ('-- Type --')
    
class Configuration(models.Model):
    app = models.CharField(
        verbose_name=_("App"), 
        max_length=255,
        validators=[
            RegexValidator(
                regex='^[a-z_][a-z0-9_]*$',
                message=_('App name not allow.'),
                code='app_name_wrong'
            )
        ]
    )
    
    model = models.CharField(
        verbose_name=_("Model"), 
        max_length=255,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z]+$',
                message=_('This field contains invalid characters.'),
                code='invalid_characters'
            )
        ]
    )
    
    status = models.IntegerField(_("Status"), choices=Status, default=Status.enable)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Configuration'
        verbose_name_plural = 'Configurations'
        ordering = ['id']
        
    def __str__(self):
        return f'{self.app}.{self.model}'
    
class Template(models.Model):
    configuration = models.ForeignKey(to=Configuration, verbose_name=_("Configuration"), on_delete=models.CASCADE)
    type = models.IntegerField(verbose_name=_("Type"),choices=TemplateType.choices)
    
    label = models.CharField(
        verbose_name=_("Label"), 
        max_length=255,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z _\-\[\]\(\)\{\}]+$',
                message=_('This field contains invalid characters.'),
                code='invalid_characters'
            )
        ]
    )
    
    column = models.CharField(
        verbose_name=_("Column"), 
        max_length=255,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z]+$',
                message=_('This field contains invalid characters.'),
                code='invalid_characters'
            )
        ]
    )
    
    value = models.CharField(
        verbose_name=_(""), 
        max_length=255,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z_]+$',
                message=_('This field contains invalid characters.'),
                code='invalid_characters'
            )
        ]
    )
    
    template_file = models.FileField(
        verbose_name=_("Template"), 
        blank=True,
        upload_to=None,
        max_length=100,
        validators=[
            
        ]
    )
    status = models.IntegerField(_("Status"), choices=Status, default=Status.enable)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Template'
        verbose_name_plural = 'Templates'
        ordering = ['id']
        
    def __str__(self):
        return f'{self.id}'
        
class Category(models.Model):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9 ]+$',
                message=_('This field contains invalid characters.'),
                code='invalid_characters'
            )
        ]
    )
    
    description = models.TextField(
        verbose_name=_("Description"),
        validators=[
            MaxLengthValidator(500),
            MinLengthValidator(10),
            RegexValidator(
                regex='^[a-zA-Z0-9 ]+$',
                message=_('This field contains invalid characters.'),
                code='invalid_characters'
            )
        ]
    )
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    status = models.IntegerField(_("Status"), choices=Status, default=Status.enable)
    
    class Meta():
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
        
    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(
        verbose_name=_("Name"),
        unique=True,
        max_length=50,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9 ]+$',
                message=_('This field contains invalid characters.'),
                code='invalid_characters'
            )
        ]
    )
    
    extra_info = models.TextField(
        verbose_name=_("Extra information"),
        validators=[
            MaxLengthValidator(500),
            MinLengthValidator(10),
            RegexValidator(
                regex='^[a-zA-Z0-9 ]+$',
                message=_('This field contains invalid characters.'),
                code='invalid_characters'
            )
        ]
    )
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    status = models.IntegerField(_("Status"), choices=Status, default=Status.enable)
    
    class Meta():
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
        ordering = ['name']
        
    def __str__(self):
        return self.name

class Product(models.Model):
    code = models.CharField(
        verbose_name=_("Code"), 
        help_text='Format (AAA-000)',
        max_length=7, 
        unique=True,
        validators=[
            MinLengthValidator(7),
            RegexValidator(
                regex='^[A-Z]{3}-[0-9]{3}$',
                message=_('Code value must match with the following pattern (3 values from A-Z, - and 3 numbers), example COD-001.'),
                code='code_not_valid'
            )
        ]
    )
    
    name = models.CharField(
        verbose_name=_("Name"), 
        max_length=50,
        validators=[
            MinLengthValidator(3),
            RegexValidator(
                regex='^[a-zA-Z0-9 ]+$',
                message=_('Name contains invalid characters, allowed characters are only (-).'),
                code='name_not_valid'
            )
        ]
    )
    
    income_price = models.DecimalField(
        verbose_name=_("Income price"), 
        max_digits=8, 
        decimal_places=2,
        validators=[
            MinValueValidator(limit_value=0)
        ]
    )
    
    outcome_price = models.DecimalField(
        verbose_name=_("Outcome price"), 
        max_digits=8, 
        decimal_places=2,
        validators=[
            MinValueValidator(limit_value=0)
        ]
    )
    
    category = models.ForeignKey(to=Category, verbose_name=_("Category"), on_delete=models.PROTECT)
    supplier = models.ForeignKey(to=Supplier, verbose_name=_("Supplier"), on_delete=models.PROTECT)
    
    extra_info = models.TextField(
        verbose_name=_("Extra information"), 
        blank=True,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9 -*@#.]+$',
                message=_('Field contains invalid characters, allowed characters are (- * @ # . )'),
                code='invalid_characters'
            ),
            MaxLengthValidator(500)
        ]
    )
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    status = models.IntegerField(_("Status"), choices=Status, default=Status.enable)
    
    class Meta():
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-createtime']
        
    def __str__(self):
        return self.code