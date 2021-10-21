from django.db     import models

from core.models   import TimeStampedModel
from users.models  import User
from places.models import Place

class Book(TimeStampedModel):
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    place        = models.ForeignKey(Place, on_delete=models.CASCADE)
    date         = models.DateField()
    start_time   = models.DateTimeField()
    end_time     = models.DateTimeField()
    head_count   = models.IntegerField()
    total_price  = models.IntegerField()
    content_type = models.CharField(max_length=50)
    content_info = models.TextField()
    status_code  = models.ForeignKey('BookStatus', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'books'
        
class BookStatus(TimeStampedModel):
    status = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'book_statuses'