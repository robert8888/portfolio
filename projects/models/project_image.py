from django.db import models

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'projects-'.format(instance.project.name, filename)

class ProjectImage(models.Model):
    project = models.ForeignKey(
        'Project', 
        default=None, 
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to = user_directory_path, 
        width_field = 'width', 
        height_field = 'height'
    )

    width = models.PositiveIntegerField()

    height = models.PositiveIntegerField()

    def __str__(self):
        return self.project.name