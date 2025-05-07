from django.shortcuts import render
from django.views import generic

from .models import Game
from accounts.models import CustomUser
from django.core.exceptions import PermissionDenied
import registry.utils as utils
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from .forms import AddGameForm


class ViewGamesView(PermissionRequiredMixin, generic.ListView):
    permission_required = ["registry.can_view_others_games", "registry.can_view_others_ratings"]
    raise_exception = True

    template_name = "registry/view.html"
    context_object_name = "game_list"

    def get_queryset(self):
        games = Game.objects.order_by("-date_time")
        return games


class GameAddFormView(PermissionRequiredMixin, generic.FormView):
    permission_required = ["registry.can_view_others_games", "registry.can_add_games", "registry.can_view_others_ratings"]
    raise_exception = True

    template_name = "registry/add_game_form.html"
    form_class = AddGameForm
    context_object_name = "players"
    success_url = reverse_lazy("registry:view")

    def form_valid(self, form):
        newGame = Game()

        player_1 = form.cleaned_data["player_1"]
        player_2 = form.cleaned_data["player_2"]
        referee = self.request.user

        utils.give_user_rating_if_no_rating(player_1)
        utils.give_user_rating_if_no_rating(player_2)
        
        if form.cleaned_data["game_result"] == "1":
            game_result_player_1 = 1
            game_result_player_2 = 0
        elif form.cleaned_data["game_result"] == "2":
            game_result_player_1 = 0
            game_result_player_2 = 1
        elif form.cleaned_data["game_result"] == "3":
            game_result_player_1 = 0.5
            game_result_player_2 = 0.5

        player_1_rating_calculator = utils.Player()
        player_1_rating_calculator.rating = player_1.rating.rating
        player_1_rating_calculator.rd = player_1.rating.rating_deviation
        player_1_rating_calculator.vol = player_1.rating.rating_volatility
        
        player_2_rating_calculator = utils.Player()
        player_2_rating_calculator.rating = player_2.rating.rating
        player_2_rating_calculator.rd = player_2.rating.rating_deviation
        player_2_rating_calculator.vol = player_2.rating.rating_volatility

        player_1_old_rating = player_1_rating_calculator.rating
        player_2_old_rating = player_2_rating_calculator.rating

        player_1_old_rating_deviation = player_1_rating_calculator.rd
        player_2_old_rating_deviation = player_2_rating_calculator.rd

        player_1_rating_calculator.update_player(
            [player_2_old_rating],
            [player_2_old_rating_deviation],
            [game_result_player_1]
        )

        player_2_rating_calculator.update_player(
            [player_1_old_rating],
            [player_1_old_rating_deviation],
            [game_result_player_2]
        )

        player_1_rating_change = player_1_rating_calculator.rating - player_1_old_rating
        player_2_rating_change = player_2_rating_calculator.rating - player_2_old_rating


        newGame.date_time = timezone.now()

        newGame.player_1 = player_1
        newGame.player_2 = player_2
        newGame.referee = referee

        newGame.player_1_rating = player_1_old_rating
        newGame.player_2_rating = player_2_old_rating

        if form.cleaned_data["ranked"]:
            newGame.player_1_rating_change = player_1_rating_change
            newGame.player_2_rating_change = player_2_rating_change

            newGame.ranked = True

        else:
            newGame.player_1_rating_change = 0
            newGame.player_2_rating_change = 0

            newGame.ranked = False

        newGame.game_result = form.cleaned_data["game_result"]

        newGame.save()


        if form.cleaned_data["ranked"]:
            player_1.rating.rating = player_1_rating_calculator.rating
            player_1.rating.rating_deviation = player_1_rating_calculator.rd
            player_1.rating.rating_volatility = player_1_rating_calculator.vol
            player_1.rating.save()
            # player_1.save()

            player_2.rating.rating = player_2_rating_calculator.rating
            player_2.rating.rating_deviation = player_2_rating_calculator.rd
            player_2.rating.rating_volatility = player_2_rating_calculator.vol
            player_2.rating.save()
            # player_2.save()


        return super().form_valid(form)
    

    
class PlayerDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = ["registry.can_view_others_ratings"]
    raise_exception = True

    template_name = "registry/detail.html"
    context_object_name = "player"
    model = CustomUser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        player = CustomUser.objects.get(pk=self.kwargs["pk"])
        utils.give_user_rating_if_no_rating(player)

        context["rating_deviation"] = round(player.rating.rating_deviation)
        context["confidence_interval_max"] = player.rating.rating + (2 * context["rating_deviation"])
        context["confidence_interval_min"] = player.rating.rating - (2 * context["rating_deviation"])

        if context["confidence_interval_min"] < 0:
            context["confidence_interval_min"] = 0

        return context
    