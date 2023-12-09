# Generated by Django 5.0 on 2023-12-08 23:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0002_alter_contract_options_contract_created_by"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="client",
            options={"verbose_name": "cliente"},
        ),
        migrations.AlterModelOptions(
            name="pos",
            options={"verbose_name": "PDV", "verbose_name_plural": "PDVs"},
        ),
        migrations.AlterModelOptions(
            name="sale",
            options={"verbose_name": "Venda"},
        ),
        migrations.AlterModelOptions(
            name="salemovement",
            options={"verbose_name": "movimento"},
        ),
        migrations.AddField(
            model_name="sale",
            name="description",
            field=models.CharField(
                blank=True, max_length=120, verbose_name="Descrição"
            ),
        ),
        migrations.AlterField(
            model_name="pos",
            name="pending_payments",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=12, verbose_name="Pendências"
            ),
        ),
        migrations.AlterField(
            model_name="sale",
            name="balance",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=12, verbose_name="Saldo"
            ),
        ),
    ]
