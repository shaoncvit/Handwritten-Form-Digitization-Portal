from django.contrib import admin
from .models import Customer, Contact_us, Category,register_table,add_Form
admin.site.site_header = "My Website"
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    # fields = ["name", "email"]

    list_display = ["id","name", "email","gender","is_registered"]
    search_fields = ["name"]
    list_filter = ["name","gender"]
    list_editable = ["email"]

class Contact_usAdmin(admin.ModelAdmin):
    list_display = ["id", "name","contact_number","message", "added_on"]
    list_filter = ["name","added_on"]
    list_editable = ["contact_number"]

class CategoryAdmin(admin.ModelAdmin):

    list_display = ["id", "cat_name", "description","added_on"]
    list_editable = ["description"]
    list_editable = ["cat_name"]

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Contact_us,Contact_usAdmin )
admin.site.register(Category, CategoryAdmin)
admin.site.register(register_table)
admin.site.register(add_Form)