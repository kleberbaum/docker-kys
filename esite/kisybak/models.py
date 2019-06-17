from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.postgres.fields import JSONField

from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList, InlinePanel, StreamFieldPanel, MultiFieldPanel, FieldPanel
from wagtail.images.blocks import ImageChooserBlock

#class Company(models.Model):
#  companyID = models.AutoField(primary_key=True)
#  companyName = models.CharField(null=True, blank=False,max_length=128)
#  companyVAT = JSONField()
#  companyAddress = models.CharField(null=True, blank=False, max_length=60)
#  companyZIP = models.CharField(null=True, blank=False, max_length=12)
#  comapnyCity = models.CharField(null=True, blank=False,max_length=60)
#  companyRating = JSONField()

class Customer(AbstractUser):
  customerID = models.AutoField(primary_key=True)
  email = models.EmailField(null=True, blank=False)
  title = models.BooleanField(null=True, blank=False)
  firstName = models.CharField(null=True, blank=False, max_length=30)
  lastName = models.CharField(null=True, blank=False, max_length=30)
  birthdate = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=False)
  telephone = models.CharField(null=True, blank=False, max_length=40)
  password = models.CharField(null=True, blank=False, max_length=512)
  address = models.CharField(null=True, blank=False, max_length=60)
  zipCode = models.CharField(null=True, blank=False, max_length=12)
  city = models.CharField(null=True, blank=False,max_length=60)
  country = models.CharField(null=True, blank=False,max_length=2)
  # company = models.ForeignKey(Company, on_delete=models.CASCADE)
  personalisation = JSONField(null=True, blank=False)
  newsletter = models.BooleanField(null=True, blank=False)
  gdpr = models.BooleanField(null=True, blank=False)
  balance = models.IntegerField(null=True, blank=False)
  loyalty = models.IntegerField(null=True, blank=False)
  achievements = JSONField(null=True, blank=False)
  rememberToken = models.CharField(null=True, blank=False, max_length=512)

  def __str__(self):
    return f"{self.first_name} {self.last_name}"

class Order(models.Model):
  orderID = models.AutoField(primary_key=True)
  orderName = models.CharField(null=True, blank=False, max_length=30)
  customerID = models.ForeignKey(Customer, on_delete=models.CASCADE)

class Item(models.Model):
  itemID = models.AutoField(primary_key=True)
  order = models.ForeignKey(Order, on_delete=models.CASCADE)
  product = models.ForeignKey(Customer, on_delete=models.CASCADE)

class Product(models.Model):
  productID = models.AutoField(primary_key=True)
  productName = models.CharField(null=True, blank=False, max_length=30)
  productPrice = models.IntegerField(null=True, blank=False)

class Invoice(models.Model):
  order = models.OneToOneField(Order, on_delete=models.CASCADE)
  invoiceName = models.CharField(primary_key=True, max_length=12) # RE-YYYY-xxxx
  invoiceCashback = JSONField(null=True, blank=False)
  invoicePaymentTime = models.IntegerField(null=True, blank=False) # max 31 days
