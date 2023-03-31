# Generated by Django 3.2.15 on 2022-11-30 16:31

import arches.app.models.fields.i18n
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("models", "8974_rr_load_performance_v2"),
    ]

    operations = [
        migrations.AddField(
            model_name="graphmodel",
            name="source_identifier",
            field=models.ForeignKey(
                blank=True, db_column="source_identifier", null=True, on_delete=models.deletion.CASCADE, to="models.graphmodel"
            ),
        ),
        migrations.AddField(
            model_name="cardmodel",
            name="source_identifier",
            field=models.ForeignKey(
                blank=True, db_column="source_identifier", null=True, on_delete=models.deletion.CASCADE, to="models.cardmodel"
            ),
        ),
        migrations.AddField(
            model_name="edge",
            name="source_identifier",
            field=models.ForeignKey(
                blank=True, db_column="source_identifier", null=True, on_delete=models.deletion.CASCADE, to="models.edge"
            ),
        ),
        migrations.AddField(
            model_name="node",
            name="source_identifier",
            field=models.ForeignKey(
                blank=True, db_column="source_identifier", null=True, on_delete=models.deletion.CASCADE, to="models.node"
            ),
        ),
        migrations.AddField(
            model_name='graphmodel',
            name='has_unpublished_changes',
            field=models.BooleanField(default=False),
        ),
    ]
