from django.test import TestCase
from django.urls import reverse
from registry.models import Game
from accounts.models import CustomUser
from django.utils import timezone
from registry.forms import AddGameForm
import datetime
from django.contrib.auth.models import Permission, Group
from registry.management.commands.create_groups import Command


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
        
class GameAddFormViewTest(TestCase):
    def setUp(self):
        self.player1 = CustomUser(email="player1@test.com", first_name="Player", last_name="One")
        self.player1.set_password("password1357")
        self.player2 = CustomUser(email="player2@test.com", first_name="Player", last_name="Two")
        self.player2.set_password("password1357")
        self.player3 = CustomUser(email="player3@test.com", first_name="Player", last_name="Three", password="password1357")
        self.player3.set_password("password1357")

        self.player1.save()
        self.player2.save()
        self.player3.save()

        create_group_command = Command()
        create_group_command.handle()

    def test_access_add_game_form_view_without_login(self):
        response = self.client.get(reverse("registry:add_game"))

        self.assertEqual(response.status_code, 403)

    def test_access_add_game_form_view_logged_in_without_permissions(self):
        self.client.login(email="player3@test.com", password="password1357")

        response = self.client.get(reverse("registry:add_game"))

        self.assertEqual(response.status_code, 403)

    def test_access_add_game_form_view_logged_in_with_proper_permissions(self):
        officerGroup = Group.objects.get(name="Officers")
        self.player1.groups.add(officerGroup)
        self.client.login(email="player1@test.com", password="password1357")

        response = self.client.get(reverse("registry:add_game"))

        self.assertEqual(response.status_code, 200)

    def test_add_game_post_request_not_logged_in(self):
        self.client.login(email="player1@test.com", password="password1357")

        response = self.client.post(reverse("registry:add_game"), {"player_1": self.player2.pk, "player_2": self.player3, "game_result": 2, "ranked": True})

        self.assertEqual(response.status_code, 403)

    def test_add_game_post_request_logged_in_with_proper_permissions_is_successful(self):
        officerGroup = Group.objects.get(name="Officers")
        self.player1.groups.add(officerGroup)
        self.client.login(email="player1@test.com", password="password1357")

        response = self.client.post(reverse("registry:add_game"), {"player_1": self.player2.pk, "player_2": self.player3, "game_result": 2, "ranked": True})

        self.assertEqual(response.status_code, 200)

    def test_add_game_post_request_logged_in_with_proper_permissions_adds_game_to_database(self):
        officerGroup = Group.objects.get(name="Officers")
        self.player1.groups.add(officerGroup)
        self.client.login(email="player1@test.com", password="password1357")

        response = self.client.post(reverse("registry:add_game"), data={"player_1": self.player2.pk, "player_2": self.player3.pk, "game_result": 2, "ranked": True})

        self.assertRedirects(response, reverse("registry:view"))

        games = Game.objects.all()
        self.assertEqual(len(games), 1)

        game = games[0]

        self.assertEqual(game.player_1, self.player2)
        self.assertEqual(game.player_2, self.player3)
        self.assertEqual(game.referee, self.player1)
        self.assertEqual(game.ranked, True)
        self.assertEqual(game.game_result, 2)
