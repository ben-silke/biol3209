from django.contrib import admin

from . import models as dna_records

# Register your models here.

admin.register(dna_records.DatabaseReference)
admin.register(dna_records.Sequence)
admin.register(dna_records.Feature)
admin.register(dna_records.Database)
admin.register(dna_records.GenbankRecord)
admin.register(dna_records.EnsemblRecord)
admin.site.site_header = 'DNA Records'
