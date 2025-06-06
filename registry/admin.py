from django.contrib import admin
from .models import Game
from .models import Rating

class GameAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Player 1", {"fields": ["player_1"]}),
        ("Player 2", {"fields": ["player_2"]}),
        ("Referee", {"fields": ["referee"]}),
        ("Game Result", {"fields": ["game_result"]}),
        ("Date and Time", {"fields": ["date_time"]}),
        ("Player 1 Rating", {"fields": ["player_1_rating"]}),
        ("Player 1 Rating Change", {"fields": ["player_1_rating_change"]}),
        ("Player 2 Rating", {"fields": ["player_2_rating"]}),
        ("Player 2 Rating Change", {"fields": ["player_2_rating_change"]}),
    ]
    list_display = ["date_time", "player_1_rating", "player_2_rating"]
    list_filter = ["date_time"]
    search_fields = []

class RatingAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Player", {"fields": ["player"]}),
        ("Rating", {"fields": ["rating"]}),
        ("Rating Deviation", {"fields": ["rating_deviation"]}),
        ("Rating Volatility", {"fields": ["rating_volatility"]}),
    ]

    list_display = ["player", "rating"]

admin.site.register(Game, GameAdmin)
admin.site.register(Rating, RatingAdmin)