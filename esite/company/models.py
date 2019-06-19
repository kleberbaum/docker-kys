from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

from django.contrib.postgres.fields import JSONField

from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList, InlinePanel, StreamFieldPanel, MultiFieldPanel, FieldPanel
from wagtail.images.blocks import ImageChooserBlock

class Company(models.Model):
  companyID = models.AutoField(primary_key=True)
  companyName = models.CharField(null=True, blank=False,max_length=128)
  companyVAT = JSONField(null=True, blank=False)
  companyAddress = models.CharField(null=True, blank=False, max_length=60)
  companyZIP = models.CharField(null=True, blank=False, max_length=12)
  comapnyCity = models.CharField(null=True, blank=False,max_length=60)
  companyRating = JSONField(null=True, blank=False)

  def __str__(self):
    return self.companyName