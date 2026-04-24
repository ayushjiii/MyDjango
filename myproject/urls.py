from django.urls import path, include
from apod.views import history, home, detail, toggle_favourite,favourites,signup_view
from django.contrib import admin

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),
    path('signup/',signup_view, name = "signup"),
    path('history/', history, name="history"),
    path('apod/<int:id>/', detail, name = "detail"),
    path('favourite/<int:id>/', toggle_favourite, name = "toggle_favourite"),
    path('favourites/',favourites, name = "favourites")
]  