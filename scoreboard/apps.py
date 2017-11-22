from django.apps import AppConfig
from django.core import mail
#from . import models
import datetime
import sqlite3

# def handle_expired_challenges():
#     expiredChallenges = models.Challenge.select_for_update().filter(expiration_date__lt = datetime.datetime.now())
#     for challenge in expiredChallenges:
#         print("Expired challenge: " +  challenge)
#         challenge.contender_score = 0
#         challenge.challengee_score = 3
#         challenge.game_date = challenge.expiration_date
#         challenge.challenge_open = False
#         #send contender and challengee an email that their challenge expired

class ScoreboardConfig(AppConfig):
    name = 'scoreboard'
    def app_ready():
        handle_expired_challenges()
        #cyclic tasks
        #check if challenges expired