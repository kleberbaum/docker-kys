from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)

# Register your models here.

from .models import Customer

class CustomerAdmin(ModelAdmin):
    model = Customer
    menu_label = "Customers"
    menu_icon = "user"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    #list_display = ("email", "lastname")
    #search_fields = ("email", "lastname")

modeladmin_register(CustomerAdmin)
