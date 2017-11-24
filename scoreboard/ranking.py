from django.db.models import Q
from . import models
from operator import itemgetter


def get_Ranking():
    players = models.Profile.objects.filter(activePlayer=True).order_by('-points')
    ranking = []
    rank = 1
    for i in range(0,len(players)):
        ranking.append({'rank':rank,'player':players[i].user.username,'points':players[i].points})
        rank = rank +1
    for i in range(1,len(ranking)):
        if ranking[i-1]['points'] == ranking[i]['points']:
            ranking[i]['rank'] = ranking[i-1]['rank']
        else:
            ranking[i]['rank'] = ranking[i-1]['rank'] + 1
    return ranking

def everlasting_Ranking():
    players = models.Profile.objects.filter(activePlayer=True)
    ranking = []
    for player in players:
        points = models.Challenge.objects.filter((Q(contender=user) | Q(challengee = user)) & Q(challenge_open=False)).count()
        ranking.append({'rank':0,'player':player.user.username,'points':points})
    #sort by points
    ranking = sorted(ranking,key=itemgetter('points'),reverse = True)
    ranking[0]['rank'] = 1
    for i in range(1,len(ranking)):
        if ranking[i-1]['points'] == ranking[i]['points']:
            ranking[i]['rank'] = ranking[i-1]['rank']
        else:
            ranking[i]['rank'] = ranking[i-1]['rank'] + 1

    return ranking
    
def getPointsAgainst(user,against,endDate=None):       
    # the last 3 games by the user against user2
    if endDate is not None:
        games = models.Challenge.objects.filter(Q(challenge_open = False) &
                                                 (Q(contender = user) | Q(challengee = user)) &
                                                 (Q(contender = against) | Q(challengee = against)) &
                                                 Q(game_date__lte = endDate)).order_by('-game_date')[:3]
    else:
        games = models.Challenge.objects.all().filter(Q(challenge_open = False) &
                                                 (Q(contender = user) | Q(challengee = user)) &
                                                 (Q(contender = against) | Q(challengee = against))).order_by('-game_date')[:3]
    
    count = games.count()

    if count == 3:
        return 3*gamePoints(user,games[0]) + 2*gamePoints(user,games[1]) + gamePoints(user,games[2])
    elif count == 2:
        return 3*gamePoints(user,games[0]) + 2*gamePoints(user,games[1])
    elif count == 1:
        return 3*gamePoints(user,games[0])
    return 0

def updatePoints():
    #loop over every active user and get the last 3 games
    profiles = models.Profile.objects.filter(activePlayer = True)
    for player in profiles:
        oldPoints = player.points
        points = 0
        user = player.user
        for player2 in profiles.exclude(user = player.user):
            user2 = player2.user            
            points = points + getPointsAgainst(user,user2)

        #save user points
        player.points = points
        if(points > oldPoints):
            player.trend = 1
        elif points < oldPoints:
            player.trend = -1
        player.save()

def getPoints(user,endDate = None):
    profiles = models.Profile.objects.filter(activePlayer=True)
    points = 0
    for player in profiles.exclude(user = user):
        user2 = player.user
        points = points+getPointsAgainst(user,user2,endDate)
    return points

def winner(challenge):
    if challenge.contender_score > challenge.challengee_score:
        return challenge.contender
    return challenge.challengee

def gamePoints(user,challenge):
    if winner(challenge) == user:
        return 1.0
    return 0
