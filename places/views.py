import json
from datetime             import datetime, timedelta

from django.http.response import JsonResponse
from django.views         import View
from django.db.models     import Q

from places.models        import Place
from books.models         import Book, BookStatus
from users.utils          import login_required


class PlaceListView(View):    
    def get(self, request):
        try: 
            menu     = request.GET.get('menu', None)
            category = request.GET.get('category', None)
            keyword  = request.GET.get('keyword', None)
            order    = request.GET.get('order', 'id')
        
            q=Q()
            
            if menu:
                q &= Q(category__menu__id = menu)
            
            if category:
                q &= Q(category__id = category)
                
            if keyword:
                q &= Q(name__contains=keyword)
            
            places = Place.objects.filter(q).order_by(order)

            result = [{
                'id'        : place.id,
                'place_name': place.name,
                'category'  : place.category.name,
                'price'     : place.price,
                'capacity'  : place.capacity,
                'city'      : place.city.name,
                'parking'   : place.parking,
                'url'       : [image.url for image in place.image_set.all()],
                } for place in places]
            
            return JsonResponse({'result' : result}, status=200)
        
        except Place.DoesNotExist:
            return JsonResponse({'message' : 'DOES_NOT_FOUND'}, status=400)
        
        except TypeError:
            return JsonResponse({'message' : 'TYPE_ERROR'}, status=400)
        
        except ValueError:
            return JsonResponse({'message' : 'VALUE_ERROR'}, status=400)

class PlaceDetailView(View):
    def get(self, request, place_id):
        try:
            place = Place.objects.get(id=place_id)

            result = {
                'id'            : place.id,
                'place_name'    : place.name,
                'category'      : place.category.name,
                'city'          : place.city.name,
                'minimum_time'  : place.minimum_time,
                'description'   : place.description,
                'capacity'      : place.capacity,
                'size'          : place.size,
                'floor'         : place.floor,
                'price'         : place.price,
                'parking'       : place.parking,
                'url'           : [image.url for image in place.image_set.all()],
                'location_info' : place.location_info
            }
            return JsonResponse({'result' : result}, status=200)
        
        except Place.DoesNotExist:
            return JsonResponse({'message' : 'DOES_NOT_FOUND'}, status=400)
        
        except ValueError:
            return JsonResponse({'message' : 'VALUE_ERROR'}, status=400)

class PlaceCalendarView(View):
    @login_required
    def get(self, request, place_id):
        try:
            if not Place.objects.filter(id=place_id).exists():
                return JsonResponse({"message":"INVALID_PLACE_ID"}, status=404)

            time = request.GET.get('time', None)
            days = int(request.GET.get('days', 60))

            current_time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
            day_limit    = (current_time + timedelta(days)).date()

            books = Book.objects.filter(
                place_id           = place_id,
                status_code_id__in = [BookStatus.Status.PENDING.value, BookStatus.Status.CONFIRMED.value], 
                start_time__gt     = current_time,
                end_time__lt       = day_limit
            )

            result = [{
                    'start_time' : book.start_time,
                    'end_time'   : book.end_time,
                    'usage_time' : str(book.end_time - book.start_time).split(":")[0]
                } for book in books]
            return JsonResponse({'result': result})

        except ValueError:
            return JsonResponse({'message':'VALUE_ERROR'}, status=400)

        except TypeError:
            return JsonResponse({'message':'TYPE_ERROR'}, status=400)
