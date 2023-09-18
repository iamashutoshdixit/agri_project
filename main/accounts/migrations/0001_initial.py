# Generated by Django 4.1.3 on 2022-11-23 17:51

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Reimbursement",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("invoice_date", models.DateTimeField()),
                ("invoice_no", models.IntegerField()),
                ("items", models.JSONField()),
                ("amount", models.IntegerField()),
                (
                    "photos",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.URLField(), blank=True, null=True, size=None
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[(0, "Open"), (1, "Rejected"), (2, "Approved")],
                        default=0,
                    ),
                ),
                ("remarks", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="reimbursement_approved_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Reimbursements",
                "verbose_name_plural": "Reimbursements",
            },
        ),
    ]