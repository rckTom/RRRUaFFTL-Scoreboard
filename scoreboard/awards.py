from django.db.models import Q
from .models import Challenge, Profile


class Awards():
    def mostGamesPlayed(self):
        players = Profile.objects.filter(active_player = True)
        
        maxContenderCount = 0
        maxChallengeeCount = 0
        maxGamesCount = 0

        for player in players:
            gamesAsContender = Challenge.objects.filter(Q(contender = player.user) & Q(challenge_open = False)).count()
            gamesAsChallengee = Challenge.objects.filter(Q(challengee = player.user) & Q(challenge_open = False)).count()
            gamesCount = gamesAsChallengee+gamesAsContender
            if gamesAsChallengee > maxChallengeeCount:
                maxChallengeeCount = gamesAsChallengee
                maxChallengeeCountUser = player
            if gamesAsContender > maxContenderCount:
                maxContenderCount = gamesAsContender
                maxContenderCountUser = player
            if gamesCount > maxGamesCount:
                maxGamesCount = gamesCount
                maxGamesCountUser = player
        
        maxGames = {'user':maxGamesCountUser,'count':maxGamesCount}
        maxContender = {'user':maxContenderCountUser,'count':maxContenderCount}
        maxChallengee = {'user':maxChallengeeCountUser,'count':maxChallengeeCount}