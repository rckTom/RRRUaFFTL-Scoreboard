from django import forms
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from . import models
from datetime import datetime, timedelta


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username', 'placeholder':"Username"}))
    password = forms.CharField(label="Password", max_length=30, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password', 'placeholder':"Password"}))

class ChallengeResultForm(forms.Form):
    def __init__(self,user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['challenge'] = forms.ModelChoiceField(models.Challenge.objects.all().filter(contender = user, challenge_open = True, game_reported=False))
        self.fields['contender_score'] = forms.IntegerField()
        self.fields['challengee_score'] = forms.IntegerField()
        self.fields['game_date'] = forms.DateTimeField()

        self.fields['challenge'].widget.attrs = {'class':'form-control'}
        self.fields['contender_score'].widget.attrs = {'class':'form-control'}
        self.fields['challengee_score'].widget.attrs = {'class':'form-control'}
        self.fields['game_date'].widget.attrs = {'class':'form-control','id':'game_date'}
        self.fields['game_date'].input_formats = ['%d.%m.%Y %H:%M']

    def save(self,challenge_open=True):
        challenge = self.cleaned_data['challenge']
        challenge.contender_score = self.cleaned_data['contender_score']
        challenge.challengee_score = self.cleaned_data['challengee_score']
        challenge.challenge_open = challenge_open
        challenge.game_date = self.cleaned_data['game_date']
        challenge.game_reported = True
        challenge.save()
        print(challenge)

class AddChallengeForm(forms.Form):
    def __init__(self,user,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.user = user
        activeChallenges = models.Challenge.objects.all().filter(Q(contender = self.user) & Q(challenge_open = True))
        exludedUsers = []
        for challenge in activeChallenges:
            exludedUsers.append(challenge.challengee)
            exludedUsers.append(challenge.contender)

        exludedUsers.append(self.user)
        exludedUsers = list(set(exludedUsers))

        qs = models.Profile.objects.all().filter(activePlayer = True)
        for user in exludedUsers:
            qs = qs.exclude(user = user)

        self.fields['challengee'] = forms.ModelChoiceField(qs)
        self.fields['challengee'].widget.attrs = {'class':'form-control'}

    def save(self):
        challenge = models.Challenge()
        challenge.challenge_date = datetime.now()
        challenge.expiration_date = challenge.challenge_date + timedelta(days=10)
        challenge.contender = self.user
        challenge.challengee = self.cleaned_data['challengee'].user
        challenge.game_reported = False
        challenge.save()