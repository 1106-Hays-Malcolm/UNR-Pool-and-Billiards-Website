from django import forms
from accounts.models import CustomUser
from django.utils.translation import gettext as _

class AddGameForm(forms.Form):

    player_1 = forms.ModelChoiceField(queryset=CustomUser.objects)
    player_2 = forms.ModelChoiceField(queryset=CustomUser.objects)

    GAME_RESULT_CHOICES = [
        ('1', 'Player 1 Wins'),
        ('2', 'Player 2 Wins'),
        ('2', 'Draw / Tie'),
    ]

    game_result = forms.ChoiceField(widget=forms.RadioSelect, choices=GAME_RESULT_CHOICES)

    ranked = forms.BooleanField(initial=True, required=False)

    def clean(self):
        cleaned_data = super().clean()

        player_1 = cleaned_data.get("player_1")
        player_2 = cleaned_data.get("player_2")

        if player_1 and player_2:
            if player_1 == player_2:
                raise forms.ValidationError(_("Player 1 and Player 2 must be different!"), code="same_players")