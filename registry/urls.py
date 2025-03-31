from django.urls import path
from .views import ViewGamesView
from .views import add_game
from .views import GameAddFormView

app_name = "registry"
urlpatterns = [
    path("view/", ViewGamesView.as_view(), name="view"),
    path("add_game_form/", GameAddFormView.as_view(), name="game_add_form"),
    path("add_game/", add_game, name="add_game"),
]
