from django.db import models
from accounts.models import CustomUser

# The model for storing games
class Game(models.Model):

    date_time = models.DateTimeField("date and time of game")

    referee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="referee_games_set")

    player_1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="player_1_games_set")
    player_2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="player_2_games_set")

    # If ranked is True, the players' ratings will change after a game
    ranked = models.BooleanField(default=True)

    # player_1_rating and player_2_rating are the ratings of the players just before the game was played
    player_1_rating = models.IntegerField()
    player_2_rating = models.IntegerField()

    # The rating change is the difference between the player's rating before and after the game
    # Positive if rating points are gained, negative if points are lost
    player_1_rating_change = models.IntegerField()
    player_2_rating_change = models.IntegerField()

    # I'm not even sure if you can tie/draw in pool, but I put it there anyway
    class PossibleGameResults(models.IntegerChoices):
        PLAYER_1_WINS = 1
        PLAYER_2_WINS = 2
        DRAW = 3

    game_result = models.IntegerField(choices=PossibleGameResults)

    class Meta:
        permissions = [
            ("can_view_others_games", "Can view the games of other players. This permission is required to view the registry."),
            ("can_add_games", "Can add new games to the registry."),
        ]

class Rating(models.Model):
    player = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, default=None)

    rating = models.IntegerField(default=1500)
    rating_deviation = models.FloatField(default=350)
    rating_volatility = models.FloatField(default=0.06)

    class Meta:
        permissions = [
            ("can_view_others_ratings", "Can view the ratings of other players. This permission is required to view the registry.")
        ]
