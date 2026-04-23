from django.urls import path
from apod.views import history, home, detail, toggle_favourite,favourites
from django.contrib import admin

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('history/', history, name="history"),
    path('apod/<int:id>/', detail, name = "detail"),
    path('favourite/<int:id>/', toggle_favourite, name = "toggle_favourite"),
    path('favourites/',favourites, name = "favourites")
]