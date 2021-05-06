from django.db.models.signals import post_save
from django.core.cache import cache
from django.dispatch import receiver

@receiver(post_save)
def clear_the_cache(**kwargs):
    print("clear cache")
    cache.clear()