from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class TodoApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "todo_api"
    verbose_name = _("Django Todo Api")
