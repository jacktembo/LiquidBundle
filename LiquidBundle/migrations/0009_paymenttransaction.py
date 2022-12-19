# Generated by Django 4.1.4 on 2022-12-19 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LiquidBundle", "0008_kazangsession"),
    ]

    operations = [
        migrations.CreateModel(
            name="PaymentTransaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("session_uuid", models.CharField(max_length=255)),
                ("phone_number", models.CharField(max_length=255)),
                ("amount", models.FloatField()),
                ("reference_number", models.CharField(max_length=255)),
            ],
        ),
    ]
