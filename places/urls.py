from django.urls import path

from places.views import PlaceListView, PlaceDetailView, PlaceCalendarView

urlpatterns = [
    path('', PlaceListView.as_view()),
    path('/<int:place_id>', PlaceDetailView.as_view()),
    path('/<int:place_id>/calendar', PlaceCalendarView.as_view())
]
