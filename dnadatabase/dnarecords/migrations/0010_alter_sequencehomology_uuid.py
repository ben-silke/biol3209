# Generated by Django 4.1.1 on 2022-09-27 08:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("dnarecords", "0009_alter_sequencehomology_uuid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sequencehomology",
            name="uuid",
            field=models.UUIDField(
                default=uuid.UUID("22e1aa0d-5484-4818-af70-c3a69117907f")
            ),
        ),
    ]
