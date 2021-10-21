import json

from django.http.response import JsonResponse
from django.views         import View

from places.models        import Place

class PlaceListView(View):    
    def get(self, request):
        try:
            filter_prefixes = {
                'menu'     : 'category__menu_id',
                'category' : 'category_id'
            }
            
            filter_set = {filter_prefixes.get(key) : value[0] for (key, value) in dict(request.GET).items()}

            places = Place.objects.filter(**filter_set)
            
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
            return JsonResponse({'message' : 'TYPE_ERROR'}, status=400)

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