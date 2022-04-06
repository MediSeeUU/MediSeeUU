# from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models.medicine import Medicine

class MedicineAdmin(admin.ModelAdmin):
  list = ('eu_nr', 'ema_nr', 'legal_basis', 'legal_scope', 'atc_code', 'prime', 'orphan', 'atmp', 'ema_url')

  admin.site.register(Medicine)