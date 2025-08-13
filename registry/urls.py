from django.urls import path
from .views import ViewGamesView
from .views import GameAddFormView
from .views import PlayerDetailView
from .views import ListOfficersView
from .views import AddOfficersFormView
from .views import DemoteOfficerView
from .views import AddCaptainFormView
from .views import DemoteCaptainView
from .views import ListCaptainView

app_name = "registry"
urlpatterns = [
    path("view/", ViewGamesView.as_view(), name="view"),
    path("add_game/", GameAddFormView.as_view(), name="add_game"),
    # path("add_game/", add_game, name="add_game"),
    path("detail/<int:pk>", PlayerDetailView.as_view(), name="detail"),
    path("officer_list", ListOfficersView.as_view(), name="officer_list"),
    path("add_officer", AddOfficersFormView.as_view(), name="add_officer"),
    path("demote_officer", DemoteOfficerView.as_view(), name="demote_officer"),
    path("add_captain", AddCaptainFormView.as_view(), name="add_captain"),
    path("demote_captain", DemoteCaptainView.as_view(), name="demote_captain"),
    path("captain_list", ListCaptainView.as_view(), name="captain_list"),

]
