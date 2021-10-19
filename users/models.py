from django.db   import models

from core.models import TimeStampedModel

class User(TimeStampedModel):
    kakao_id      = models.CharField(max_length=50, unique=True)
    nickname      = models.CharField(max_length=50, blank=True)
    profile_image = models.URLField(null=True, blank=True)
    email         = models.CharField(max_length=100, blank=True)
    age_range     = models.CharField(max_length=10, blank=True)
    
    class Meta:
        db_table = 'users'
        
