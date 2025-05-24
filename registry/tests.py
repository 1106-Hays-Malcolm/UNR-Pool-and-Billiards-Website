from django.test import TestCase
from django.urls import reverse
from registry.models import Game
from accounts.models import CustomUser
from registry.forms import AddGameForm
from django.contrib.auth.models import Group
from registry.management.commands.create_groups import Command
from registry.views import ListOfficersView

# My tests
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

class ListOfficerViewTests(TestCase):
    def setUp(self):
        # Create the groups
        command = Command()
        command.handle()

        self.officer = CustomUser(email="player1@test.com", first_name="Player", last_name="One")
        self.officer.set_password("password1357")

        self.normal_user = CustomUser(email="player2@test.com", first_name="Player", last_name="Two")
        self.normal_user.set_password("password1357")
        
        self.captain = CustomUser(email="player3@test.com", first_name="Player", last_name="Three")
        self.captain.set_password("password1357")

        self.officer.save()
        self.normal_user.save()
        self.captain.save()

        officer_group = Group.objects.get(name="Officers")
        captain_group = Group.objects.get(name="Captains")

        self.officer.groups.add(officer_group)
        self.captain.groups.add(captain_group)

    def test_officer_list_view_status_code_not_signed_in(self):
        response = self.client.get(reverse("registry:officer_list"))

        self.assertEqual(response.status_code, 403)

    def test_officer_list_view_status_code_signed_in_without_proper_permissions(self):
        # Log in as a normal user without permissions
        self.client.login(email="player2@test.com", password="password1357")
        response = self.client.get(reverse("registry:officer_list"))

        self.assertEqual(response.status_code, 403)

    def test_officer_list_view_status_code_signed_in_with_proper_permissions(self):
        # Log in as a captain
        self.client.login(email="player3@test.com", password="password1357")
        response = self.client.get(reverse("registry:officer_list"))

        self.assertEqual(response.status_code, 200)

    def test_officer_list_view_get_list_of_officers(self):
        officer_list_view = ListOfficersView()
        officer_list = officer_list_view.get_queryset()

        self.assertEqual(len(officer_list), 1)
        self.assertEqual(officer_list[0], self.officer)

    def test_officer_list_view_get_list_of_officers_with_no_officers(self):
        self.officer.delete()

        officer_list_view = ListOfficersView()
        officer_list = officer_list_view.get_queryset()

        self.assertEqual(len(officer_list), 0)