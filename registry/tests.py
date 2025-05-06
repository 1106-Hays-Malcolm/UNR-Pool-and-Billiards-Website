from django.test import TestCase
from django.urls import reverse
from registry.models import Game
from accounts.models import CustomUser
from django.utils import timezone
from registry.forms import AddGameForm
import datetime


class AddGameFormTest(TestCase):
    def setUp(self):
        self.player1 = CustomUser(email="player1@test.com", first_name="Player", last_name="One", password="password1357")
        self.player2 = CustomUser(email="player2@test.com", first_name="Player", last_name="Two", password="password1357")

        self.player1.save()
        self.player2.save()

    def test_add_game_different_players(self):

        form = AddGameForm(data={'player_1': self.player1.pk, 'player_2': self.player2.pk, 'game_result': '1', 'ranked': True})

        self.assertTrue(form.is_valid())

    def test_add_game_same_players(self):
        form = AddGameForm(data={'player_1': self.player1.pk, 'player_2': self.player1.pk, 'game_result': '1', 'ranked': True})

        self.assertFalse(form.is_valid())
        
