from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):

        new_group, created = Group.objects.get_or_create(name='Officers')
        officerPermissionNames = ["can_view_others_games", "can_add_games", "can_view_others_ratings"]

        for name in officerPermissionNames:
            permission = Permission.objects.get(codename=name)
            new_group.permissions.add(permission)
