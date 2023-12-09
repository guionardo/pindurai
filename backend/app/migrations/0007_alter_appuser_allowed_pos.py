# Generated by Django 5.0 on 2023-12-09 14:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0006_appuser_allowed_pos"),
    ]

    operations = [
        migrations.AlterField(
            model_name="appuser",
            name="allowed_pos",
            field=models.ManyToManyField(
                blank=True, to="app.pos", verbose_name="PDV vinculados"
            ),
        ),
    ]