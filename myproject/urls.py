from django.urls import path, include
<<<<<<< HEAD
from apod.views import history, home, detail, toggle_favourite,favourites,signup_view
=======
from apod.views import history, home, detail, toggle_favourite,favourites
>>>>>>> eba354e05448cb8ae6fc4742b9e30d08c8dbe57c
from django.contrib import admin

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),
<<<<<<< HEAD
    path('signup/',signup_view, name = "signup"),
=======
>>>>>>> eba354e05448cb8ae6fc4742b9e30d08c8dbe57c
    path('history/', history, name="history"),
    path('apod/<int:id>/', detail, name = "detail"),
    path('favourite/<int:id>/', toggle_favourite, name = "toggle_favourite"),
    path('favourites/',favourites, name = "favourites")
]  