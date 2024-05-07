# Generated by Django 4.2.11 on 2024-04-30 10:42

import django.db.models.deletion
from django.db import migrations, models
from django.db.models import F, Max


JSONLD_IMPORT_MODULE_PK = "1ae62c48-7e56-4df7-a433-2042c6acdf0c"


class Migration(migrations.Migration):

    dependencies = [
        ("models", "10709_refresh_geos_by_transaction"),
    ]

    def add_jsonld_module(apps, schema_editor):
        ETLModule = apps.get_model("models", "ETLModule")
        max_helpsortorder = (
            ETLModule.objects.aggregate(max_helpsortorder=Max(F("helpsortorder")))
        )["max_helpsortorder"]

        # update_or_create() with defaults to prevent IntegrityError
        # https://code.djangoproject.com/ticket/35425
        ETLModule.objects.update_or_create(
            pk=JSONLD_IMPORT_MODULE_PK,
            defaults={
                "name": "Import JSON-LD",
                "icon": "fa fa-upload",
                "etl_type": "import",
                "component": "views/components/etl_modules/jsonld-importer",
                "componentname": "jsonld-importer",
                "modulename": "jsonld_importer.py",
                "classname": "JSONLDImporter",
                "config": {"bgColor": "#726a5b", "circleColor": "#9f9580", "show": True},
                "reversible": False,  # does not support un-overwriting a resource
                "slug": "jsonld-importer",
                "description": "Import a zip archive of JSON-LD resources to Arches",
                "helptemplate": "jsonld-importer-help",
                "helpsortorder": max_helpsortorder + 1,
            }
        )

    def remove_jsonld_module(apps, schema_editor):
        ETLModule = apps.get_model("models", "ETLModule")
        ETLModule.objects.filter(pk=JSONLD_IMPORT_MODULE_PK).delete()


    operations = [
        migrations.RunPython(add_jsonld_module, remove_jsonld_module),
        migrations.AlterField(
            model_name="loaderrors",
            name="node",
            field=models.ForeignKey(
                blank=True, db_column="nodeid", null=True, on_delete=django.db.models.deletion.CASCADE, to="models.node"
            ),
        ),
        migrations.AlterField(
            model_name="loaderrors",
            name="nodegroup",
            field=models.ForeignKey(
                blank=True, db_column="nodegroupid", null=True, on_delete=django.db.models.deletion.CASCADE, to="models.nodegroup"
            ),
        ),
    ]
