from django.contrib import admin

from . import models as gene


# Register your models here.


# Register your models here.


admin.register(gene.Gene)
admin.register(gene.CDS)
admin.register(gene.GeneDatabaseReference)
admin.register(gene.CdsDatabaseReference)
