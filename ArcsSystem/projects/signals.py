from .models import Project
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Project)
def generate_image_dir(sender, instance, created, **kwargs):
    if created:
        path = settings.MEDIA_ROOT + '/images/projects/' + str(instance.id)
        os.makedirs(path)
        instance.image_dir = '/media/images/projects/' + str(instance.id)
        instance.save()
