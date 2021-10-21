from django.urls import path

from books.views import BookPlaceView

urlpatterns = [
    path('', BookPlaceView.as_view())
]