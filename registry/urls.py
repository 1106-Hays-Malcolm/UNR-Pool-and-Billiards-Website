from django.urls import path
from .views import ViewGamesView
from .views import add_game
from .views import GameAddFormView
from .views import PlayerDetailView

app_name = "registry"
urlpatterns = [
    path("view/", ViewGamesView.as_view(), name="view"),
    path("add_game_form/", GameAddFormView.as_view(), name="game_add_form"),
    path("add_game/", add_game, name="add_game"),
    path("detail/<int:pk>", PlayerDetailView.as_view(), name="detail"),
]
