from django.db import models

# Create your models here.
class concept(models.Model):
    uuid = models.UUIDField(primary_key=True)

    class Meta:
        abstract = True
