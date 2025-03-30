from django.shortcuts import render
from django.views import generic

from .models import Game


class ViewGames(generic.ListView):
    template_name = "registry/view.html"
    context_object_name = "game_list"

    def get_queryset(self):
        games = Game.objects.order_by("-date_time")
        return games

