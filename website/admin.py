from django.contrib import admin

# MODELS
from website.models import CsvSavedData, CustomUser, Vendor_profile,Members
from import_export.admin import ImportExportModelAdmin

class CsvDataAdmin(ImportExportModelAdmin):
    list_display = ["first_name", "last_name", "email", "mobile", "address", "suburb", "state", "postal", "gender","DOB"]

# Register your models here.
admin.site.register(CsvSavedData, CsvDataAdmin)
admin.site.register(CustomUser)
admin.site.register(Vendor_profile,)
admin.site.register(Members)