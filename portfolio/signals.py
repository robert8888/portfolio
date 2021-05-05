from django.db.models.signals import post_save
from django.core.cache import cache

print('imported')
@receiver(post_save)
def clear_the_cache(**kwargs):
    print("works")
    cache.clear()