from django.http import *
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import  render_to_string

from django.views import View
import django.core.mail as mail
from jchart import Chart
from jchart.config import Axes, DataSet, rgba
import uuid
from . import forms
from . import models
from . import ranking as rank
from . import statistics as stat
import datetime


def index(request):
    return render(request, 'index.html', {})

def thanks(request):
    return render(request, 'thanks.html')

def ranking(request):
    rank.updatePoints()
    ranking = rank.get_Ranking()
    return render(request, 'ranking.html',{'ranking':ranking})

def all_games(request):
    games = models.Challenge.objects.all()
    return render(request,'all_games.html',{'challenges':games})

def points_overview(request):
    users = models.Profile.objects.filter(activePlayer=True).order_by('user')
    usernames = []
    table = []
    for user in users:
        usernames.append(user.user.username)
    header = []
    header.append('')
    header.extend(usernames)
    table.append(header)
    print(table)
    for user in users:
        points = []
        points.append(user.user.username)
        for user2 in users:
            if user == user2:
                points.append("")
            else:
                points.append(rank.getPointsAgainst(user.user,user2.user))
        table.append(points)
    return render(request, 'pointOverview.html', {'users': usernames,'table':table})

def awards(request):
    x = [1,2,3,4,5,5,6,7,8,9,9]
    return render(request, 'awards.html', {'awards':x})

def statistics(request):
    class ActivityGraph(Chart):
        chart_type = 'line'
        def __init__(self,user):
            super().__init__()
            self.user = user
            (self.x,self.y) = stat.daily_activity()
            if(self.user.is_authenticated()):
                (self.userx,self.usery) = stat.daily_user_activity(self.user)

        def get_labels(self, **kwargs):
            labels = []
            for date in self.x:
                labels.append(date.strftime('%d.%m.%y'))
            return labels

        def get_datasets(self, **kwargs):
            data = []
            datasets = []
            datasets.append(DataSet(
                color=(0,80,255),
                label='Activity of all users',
                type='line',
                data=self.y))
            if self.user.is_authenticated():
                datasets.append(DataSet(
                    color=(150,150,580),
                    label='Your activity',
                    type='line',
                    data=self.usery
                ))
            return datasets
    class WeeklyActivityGraph(Chart):
        chart_type = 'line'
        def __init__(self,user):
            super().__init__()
            self.user = user
            (self.x,self.y) = stat.activity()
            if(self.user.is_authenticated()):
                (self.userx,self.usery) = stat.user_activity(self.user)

        def get_labels(self, **kwargs):
            labels = []
            for date in self.x:
                labels.append(date.strftime('KW %W / %Y'))
            return labels

        def get_datasets(self, **kwargs):
            data = []
            datasets = []
            datasets.append(DataSet(
                color=(0, 50, 255),
                label='Activity of all users',
                type='line',
                data=self.y))
            if self.user.is_authenticated():
                datasets.append(DataSet(
                    label='Your activity',
                    type='line',
                    data=self.usery
                ))
            return datasets
    class UserPointHistory(Chart):
        chart_type = 'line'
        def __init__(self,user):
            super().__init__()
            self.user = user
            if(self.user.is_authenticated()):
                (self.x,self.y) = stat.userPointHistory(user)

        def get_labels(self, **kwargs):
            labels = []
            if self.user.is_authenticated:
                for date in self.x:
                    labels.append(date.strftime('KW %W / %Y'))
            return labels

        def get_datasets(self, **kwargs):
            data = []
            datasets = []
            if self.user.is_authenticated:
                datasets.append(DataSet(
                    label='Point History',
                    type = 'line',
                    data = self.y))
            return datasets
            
    gameStats = stat.gameStats(request.user)
    return render(request, 'statistics.html', {'chart_daily':ActivityGraph(request.user),'chart_weekly':WeeklyActivityGraph(request.user),'chart_userHistory':UserPointHistory(request.user),'game_stats':gameStats})

@login_required
def challenge(request):
    current_user = request.user
    if current_user.is_authenticated():
        if request.method == 'POST':
            form = forms.AddChallengeForm(current_user,request.POST)
            if form.is_valid():
                if form.cleaned_data['challengee'].user.email is not None:
                    message = mail.EmailMessage(subject = current_user.username + ' has challenged you',body = 'Test', to=[form.cleaned_data['challengee'].user.email])
                    message.content_subtype = "html"
                    message.send()
                form.save()
                return HttpResponseRedirect('/thanks')
        else:
            form = forms.AddChallengeForm(current_user)
        return render(request, 'add_challenge.html',{'form':form})

@login_required
def add_challenge_result(request):
    current_user = request.user
    openChallenges = models.Challenge.objects.filter(contender = current_user, challenge_open = True, game_reported=False)
    print(openChallenges)
    if current_user.is_authenticated():
        if request.method == 'POST':
            form = forms.ChallengeResultForm(current_user,request.POST)
            if form.is_valid():
                #generate token and send email
                token = uuid.uuid4()
                newEntry = models.GameResultValidation()
                newEntry.token = token
                newEntry.report_date = datetime.datetime.now()
                newEntry.game = form.cleaned_data['challenge']
                newEntry.expiration_date = newEntry.report_date+datetime.timedelta(days=10)
                message = mail.EmailMessage(subject="Game result",
                                            body=render_to_string('report_mail.html',
                                                                 {'contender': 'Contender','token':newEntry.token}),
                                            to=[newEntry.game.challengee.email])
                message.content_subtype = "html"
                message.send()
                newEntry.save()
                form.save()
                rank.updatePoints()
                return HttpResponseRedirect('/thanks/')
        else:
            form = forms.ChallengeResultForm(current_user)
        return render(request, 'add_challenge_result.html',{'form':form})

@login_required
def my_challenges(request):
    activeUser = request.user
    openChallenges_contender = models.Challenge.objects.filter(Q(contender = activeUser) & Q(challenge_open = True))
    openChallenges_challengee = models.Challenge.objects.filter(Q(challengee = activeUser) & Q(challenge_open = True))
    return render(request, 'my_challenges.html', {'challengesContender':openChallenges_contender,'challengesChallengee':openChallenges_challengee})

class ReportConfirmation(View):
    def get(self,request):
        try:
            token = request.GET['token']
            print(token)
            entry = models.GameResultValidation.objects.get(token = token)
            entry.game.challenge_open = False
            entry.game.save()
            entry.delete()
            return HttpResponseRedirect(redirect_to="/thanks/")
        except ObjectDoesNotExist:
            return HttpResponseNotFound(content="Error")