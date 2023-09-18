from django.db import models


class BaseTemplate(models.Model):
    """
    Base template containing fields common to all models
    """

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseTemplateWithActor(BaseTemplate):
    """
    Base template containing fields common to all models
    """

    created_by = models.ForeignKey("users.User", on_delete=models.PROTECT, null=True)

    class Meta:
        abstract = True
