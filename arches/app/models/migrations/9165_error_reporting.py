# Generated by Django 3.2.15 on 2023-01-09 21:50

import arches.app.models.fields.i18n
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("models", "9075_external_oauth"),
    ]

    operations = [
        migrations.CreateModel(
            name="LoadErrors",
            fields=[
                ("type", models.TextField(blank=True, null=True)),
                ("value", models.TextField(blank=True, null=True)),
                ("source", models.TextField(blank=True, null=True)),
                ("error", models.TextField(blank=True, null=True)),
                ("message", models.TextField(blank=True, null=True)),
                ("datatype", models.TextField(blank=True, null=True)),
                ("load_event", models.ForeignKey(db_column="loadid", on_delete=django.db.models.deletion.CASCADE, to="models.loadevent")),
                ("node", models.ForeignKey(db_column="nodeid", null=True, on_delete=django.db.models.deletion.CASCADE, to="models.node")),
                (
                    "nodegroup",
                    models.ForeignKey(
                        db_column="nodegroupid", null=True, on_delete=django.db.models.deletion.CASCADE, to="models.nodegroup"
                    ),
                ),
            ],
            options={
                "db_table": "load_errors",
                "managed": True,
            },
        ),
    ]
