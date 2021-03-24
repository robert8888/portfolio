from django.db import models
from django.contrib.postgres.search import SearchVectorField

class ProjectSearchAutocomplete(models.Model):
    term = models.CharField(
        max_length = 255,
    )

    language_code = models.CharField(
        max_length = 16
    )

    type = models.CharField(
        max_length = 100
    )

    source_id = models.PositiveIntegerField()

    search_vector = SearchVectorField(null=True)

    class Meta:
        db_table = 'app_projects_project_search_auto'

