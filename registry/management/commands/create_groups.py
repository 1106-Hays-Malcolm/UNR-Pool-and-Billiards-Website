from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):

        officer_group, created = Group.objects.get_or_create(name='Officers')
        captain_group, created = Group.objects.get_or_create(name='Captains')
        normal_user_group, created = Group.objects.get_or_create(name='Normal Users')
        president_group, created = Group.objects.get_or_create(name='President')

        officerPermissionNames = ["can_view_others_games",
                                  "can_add_games",
                                  "can_view_others_ratings",
                                  "able_to_be_demoted_as_officer",
                                  "eligible_to_be_captain",
                                  ]

        captainPermissionNames = ["can_view_officers_list",
                                  "can_manage_officer_status",
                                  "can_view_others_games",
                                  "can_add_games",
                                  "can_view_others_ratings",
                                  "able_to_be_demoted_as_captain",
                                  ]

        presidentPermissionNames = ["can_manage_captain_status",
                                    "can_view_others_games",
                                    "can_view_others_ratings",
                                    "can_add_games",
                                    "can_view_officers_list",
                                    ]

        normalUserPermissionNames = ["eligible_to_be_officer"
                                    ]

        for name in officerPermissionNames:
            permission = Permission.objects.get(codename=name)
            officer_group.permissions.add(permission)

        for name in captainPermissionNames:
            permission = Permission.objects.get(codename=name)
            captain_group.permissions.add(permission)

        for name in normalUserPermissionNames:
            permission = Permission.objects.get(codename=name)
            normal_user_group.permissions.add(permission)

        for name in presidentPermissionNames:
            permission = Permission.objects.get(codename=name)
            president_group.permissions.add(permission)
