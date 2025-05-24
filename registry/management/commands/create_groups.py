from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):

        officer_group, created = Group.objects.get_or_create(name='Officers')
        captain_group, created = Group.objects.get_or_create(name='Captains')

        officerPermissionNames = ["can_view_others_games", "can_add_games", "can_view_others_ratings"]
        captainPermissionNames = ["can_view_officers_list", "can_manage_officer_status"]

        for name in officerPermissionNames:
            permission = Permission.objects.get(codename=name)
            officer_group.permissions.add(permission)

        for name in captainPermissionNames:
            permission = Permission.objects.get(codename=name)
            captain_group.permissions.add(permission)
