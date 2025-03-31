from django import forms
from accounts.models import CustomUser

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