# Generated by Django 4.1.1 on 2022-09-27 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gene", "0006_cds_locus_gene_locus"),
    ]

    operations = [
        migrations.AddField(
            model_name="cds",
            name="raw_location",
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name="gene",
            name="raw_location",
            field=models.CharField(max_length=256, null=True),
        ),
    ]
