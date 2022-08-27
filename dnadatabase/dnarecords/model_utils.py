import uuid

from django.db import models


# Create your models here.
class concept(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    id = models.AutoField(primary_key=True, null=False)

    class Meta:
        abstract = True
