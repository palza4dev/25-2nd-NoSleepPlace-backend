import json
from datetime               import datetime
from json.decoder           import JSONDecodeError

from django.views           import View
from django.http            import JsonResponse
from django.db.models       import Q

from books.models           import Book, BookStatus
from places.models          import Place
from users.utils            import login_required

class BookPlaceView(View):
    @login_required
    def post(self, request):
        try:
            user       = request.user
            data       = json.loads(request.body)
            place_id   = data['place_id']
            
            if not Place.objects.filter(id=place_id).exists():
                return JsonResponse({ "message":"INVALID_PLACE"}, status=404)
            
            start_time = datetime.strptime(data['start_time'],"%Y-%m-%dT%H:%M:%S")
            end_time   = datetime.strptime(data['end_time'],"%Y-%m-%dT%H:%M:%S")
            date       = start_time.date()

            if end_time <= start_time:
                return JsonResponse({"message":"INVALID_BOOK_TIME"}, status=400)

            q1 = Q(start_time__gte=start_time) & Q(start_time__lt=end_time)
            q2 = Q(end_time__gt=start_time) & Q(end_time__lte=end_time)
            q3 = Q(start_time=start_time) & Q(end_time=end_time)           

            if Book.objects.filter(place_id=place_id).filter(q1|q2|q3).exists():
                return JsonResponse({"message":"ALREADY_BOOKED_TIME"}, status=400)

            Book.objects.create(
                place_id        = place_id,
                user_id         = user.id,
                start_time      = start_time,
                end_time        = end_time,
                date            = date,
                head_count      = data['head_count'],
                total_price     = data['total_price'],
                content_type    = data['content_type'],
                content_info    = data['content_info'],
                status_code_id  = BookStatus.Status.PENDING.value
            )
            return JsonResponse({"message":"SUCCESS"}, status=201)

        except JSONDecodeError:
            return JsonResponse({"message":"JSON_DECODE_ERROR"}, status=400)
        
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

    @login_required
    def get(self, request):
        try:
            user   = request.user
            
            filter_prefixes = {
                'status' : 'status_code__status__in'
            }

            filter_set = {filter_prefixes.get(key): value for (key, value) in dict(request.GET).items()}

            books = Book.objects.filter(user_id=user.id, **filter_set).order_by('start_time')

            result = [{
                'book_id'      : book.id,
                'name'         : book.place.name,
                'image'        : book.place.image_set.first().url,
                'content_type' : book.content_type,
                'content_info' : book.content_info,
                'head_count'   : book.head_count,
                'start_time'   : datetime.strftime(book.start_time,"%Y년 %m월 %d일 %H:00"),
                'end_time'     : datetime.strftime(book.end_time,"%H:00"),
                'host_name'    : book.place.host.name,
                'usage_time'   : int(book.total_price / book.place.price),
                'total_price'  : book.total_price,
                'status'       : book.status_code.status
                } for book in books]

            return JsonResponse({'result':result}, status=200)

        except TypeError:
            return JsonResponse({"message":"TYPE_ERROR"}, status=400)