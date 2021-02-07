from projects.models import Technology, Project
from django.db.models import Count

def get_top_technology():
    technologies_ordered = (
        Project.technologies.through
        .objects.all().values("technology_id")
        .annotate(total = Count("technology_id"))
        .order_by('total')
    )

    technologies = Technology.objects.filter(id__in = technologies_ordered.values('technology_id'))
    #print(technologies.query)

    return technologies_ordered