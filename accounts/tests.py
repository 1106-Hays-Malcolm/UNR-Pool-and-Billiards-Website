from django.test import TestCase
from accounts.models import CustomUser
from django.contrib.auth.models import Group
from registry.management.commands import create_groups
from django.urls import reverse
from .views import ListCaptainsView

class ListCaptainsViewTests(TestCase):
    def setUp(self):
        # Create the groups
        command = create_groups.Command()
        command.handle()

        captain_group = Group.objects.get(name="Officers")

        self.captain = CustomUser(email="player1@test.com", first_name="Player", last_name="One", password="password1357")
        self.normal_user = CustomUser(email="player2@test.com", first_name="Player", last_name="Two", password="password1357")

        self.captain.save()
        self.normal_user.save()

        self.captain.groups.add(captain_group)

    def test_captain_list_view_status_code(self):
        response = self.client.get(reverse("accounts:captain_list"))

        self.assertEqual(response.status_code, 200)

    def test_captain_list_view_get_list_of_captains(self):
        captain_list_view = ListCaptainsView()
        captain_list = captain_list_view.get_queryset()

        self.assertEqual(len(captain_list), 1)
        self.assertEqual(captain_list[0], self.captain)

    def test_captain_list_view_get_list_of_captains_with_no_captains(self):
        self.captain.delete()

        captain_list_view = ListCaptainsView()
        captain_list = captain_list_view.get_queryset()

        self.assertEqual(len(captain_list), 0)