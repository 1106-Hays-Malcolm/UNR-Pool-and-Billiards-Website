from django.db import models
from accounts.models import CustomUser

class Game(models.Model):

    date_time = models.DateTimeField("date and time of game")

    referee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="referee_games_set")

    player_1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="player_1_games_set")
    player_2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="player_2_games_set")

    # If ranked is True, the players' ratings will change after a game
    ranked = models.BooleanField(default=False)

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

    gameResult = models.IntegerField(choices=PossibleGameResults)