from django.contrib import admin

# Register your models here.

from . import models as gene


# Register your models here.


admin.register(gene.Gene)
admin.register(gene.CDS)
admin.register(gene.GeneDatabaseReference)
admin.register(gene.CdsDatabaseReference)
