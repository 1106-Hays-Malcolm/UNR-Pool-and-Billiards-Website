from django.urls import path
from .views import ViewGames

app_name = "registry"
urlpatterns = [
    path("view/", ViewGames.as_view(), name="view"),
]
