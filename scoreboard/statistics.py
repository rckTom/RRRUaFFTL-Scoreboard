from . import models
from django.db.models import Q,F
from collections import Counter
from datetime import datetime, timedelta,time
from . import ranking as rank

def datespan(startDate, endDate, delta=timedelta(days=1)):
    currentDate = startDate
    while currentDate <= endDate:
        yield currentDate
        currentDate += delta

def firstDayOfWeek(date):
    return date - timedelta(days=date.weekday())

def lastDayOfWeek(date):
    return date + timedelta(days=7-date.weekday())

def activity():
    daysQuerySet = models.Challenge.objects.filter(challenge_open=False).order_by('game_date')
    startDate = firstDayOfWeek(daysQuerySet.first().game_date)
    endDate = lastDayOfWeek(datetime.now())
    firstWeekDays = []

    x = []
    y = []
    for date in datespan(startDate.date(),endDate.date(),timedelta(days=7)):
        x.append(date)
        y.append(models.Challenge.objects.filter(Q(game_date__range=(firstDayOfWeek(date),date+timedelta(days=7))) &
                                                 Q(challenge_open=False)).count())
    return(x,y)

def daily_activity():
    daysQuerySet = models.Challenge.objects.filter(challenge_open=False).order_by('game_date')
    startDate = datetime.combine(daysQuerySet.first().game_date,time.min)
    endDate = datetime.combine(datetime.now(),time.max)
    firstWeekDays = []

    x = []
    y = []
    for date in datespan(startDate,endDate,timedelta(days=1)):
        x.append(date)
        y.append(models.Challenge.objects.filter(Q(game_date__range=(datetime.combine(date,time.min),datetime.combine(date,time.max))) &
                                                 Q(challenge_open=False)).count())
    return(x,y)

def daily_user_activity(user):
    daysQuerySet = models.Challenge.objects.filter(challenge_open=False).order_by('game_date')
    startDate = datetime.combine(daysQuerySet.first().game_date,time.min)
    endDate = datetime.combine(datetime.now(),time.max)
    firstWeekDays = []

    x = []
    y = []
    for date in datespan(startDate,endDate,timedelta(days=1)):
        x.append(date)
        y.append(models.Challenge.objects.filter(Q(game_date__range=(datetime.combine(date,time.min),datetime.combine(date,time.max))) &
                                                 Q(challenge_open=False) & (Q(contender = user) | Q(challengee=user))).count())
    return(x,y)

def user_activity(user):
    daysQuerySet = models.Challenge.objects.filter(challenge_open=False).order_by('game_date')
    startDate = firstDayOfWeek(daysQuerySet.first().game_date)
    endDate = lastDayOfWeek(datetime.now())
    firstWeekDays = []

    x = []
    y = []
    for date in datespan(startDate.date(),endDate.date(),timedelta(days=7)):
        x.append(date)
        y.append(models.Challenge.objects.filter(Q(game_date__range=(firstDayOfWeek(date),date+timedelta(days=7))) &
                                                 Q(challenge_open=False) & 
                                                 (Q(contender = user) | Q(challengee=user))).count())
    return(x,y)

def gameStats(user = None):
    stats = dict()
    stats['games_count'] = models.Challenge.objects.count()
    stats['open_games_count'] = models.Challenge.objects.filter(challenge_open=True).count()
    stats['closed_games_count'] = models.Challenge.objects.filter(challenge_open=False).count()
    if user.is_authenticated():
        stats['user_played_games'] = models.Challenge.objects.filter(Q(challenge_open=False) & (Q(contender=user) | Q(challengee = user))).count()
        stats['user_lost_games'] = (models.Challenge.objects.filter(Q(challenge_open=False) & Q(contender=user) & Q(contender_score__lt=F('contender_score'))).count() +
                                    models.Challenge.objects.filter(Q(challenge_open=False) & Q(challengee=user) & Q(challengee_score__lt=F('contender_score'))).count())
        stats['user_won_games'] = stats['user_played_games'] -  stats['user_lost_games']
    return stats

def userPointHistory(user):
    games = models.Challenge.objects.filter((Q(contender = user) | Q(challengee = user)) & Q(challenge_open = False)).order_by('game_date')
    dateQuery = games.values_list('game_date',flat=True)
    startDate = firstDayOfWeek(dateQuery.first())
    endDate = lastDayOfWeek(dateQuery.last())

    dates = []
    pointsList = []
    points = 0
    for day in datespan(startDate,endDate,timedelta(days=7)):
        points = rank.getPoints(user,day)
        pointsList.append(points)
        dates.append(day)

    return(dates,pointsList)