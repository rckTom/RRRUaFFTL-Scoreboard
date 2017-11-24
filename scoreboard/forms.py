from django import forms
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from . import models
from datetime import datetime, timedelta


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username', 'placeholder':"Username"}))
    password = forms.CharField(label="Password", max_length=30, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password', 'placeholder':"Password"}))

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old Password", widget = forms.PasswordInput(attrs={'class':'form-control','name':'old_password'}))
    new_password1 = forms.CharField(label='New Passowrd', widget = forms.PasswordInput(attrs={'class':'form-control','name':'new_password1'}))
    new_password2 = forms.CharField(label='Repeat new password', widget = forms.PasswordInput(attrs={'class':'form-control','name':'new_password2'}))
    
class ChallengeResultForm(forms.Form):
    def __init__(self,user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['challenge'] = forms.ModelChoiceField(models.Challenge.objects.filter(contender = user, challenge_open = True, game_reported=False))
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
        activeChallenges = models.Challenge.objects.filter((Q(contender = self.user) |  Q(challengee=self.user)) & Q(challenge_open = True))
        
        exludedUsers = []
        for challenge in activeChallenges:
            exludedUsers.append(challenge.challengee)
            exludedUsers.append(challenge.contender)

        exludedUsers.append(self.user)

        for player in models.Profile.objects.filter(activePlayer = True).exclude(user__in = exludedUsers):
            activeChallengesCount = models.Challenge.objects.filter(Q(challengee = player.user) & Q(challenge_open=True)).count()
            if activeChallengesCount >= 3:
                exludedUsers.append(player.user)

        qs = models.Profile.objects.filter(activePlayer = True).exclude(user__in = exludedUsers)

        activePlayer = models.Profile.objects.get(user=self.user)
        if activePlayer.activePlayer == True:
            self.fields['challengee'] = forms.ModelChoiceField(qs)
        else:
            self.fields['challengee'] = forms.ModelChoiceField(models.Profile.objects.none())
        self.fields['challengee'].widget.attrs = {'class':'form-control'}

    def save(self):
        challenge = models.Challenge()
        challenge.challenge_date = datetime.now()
        challenge.expiration_date = challenge.challenge_date + timedelta(days=10)
        challenge.contender = self.user
        challenge.challengee = self.cleaned_data['challengee'].user
        challenge.game_reported = False
        challenge.save()

class ProfileChangeForm(forms.Form):
    def __init__(self,profile,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.profile = profile
        self.fields['email'] = forms.EmailField(initial = profile.user.email)
        self.fields['username'] = forms.CharField(initial = profile.user.username)
        self.fields['activePlayer'] = forms.BooleanField(initial = profile.activePlayer,required=False)
        
        for fieldname, value  in self.fields.items():
            value.widget.attrs = {'class':'form-control col-sm-10'}

        self.fields['email'].widget.attrs = {'class':'form-control col-sm-10 {% if form.errors %}is-invalid{% endif %}'}
        self.fields['activePlayer'].widget.attrs = {'class':'form-check-input col-sm-10'}

    def save(self):
        self.profile.user.username = self.cleaned_data['username']
        self.profile.activePlayer = self.cleaned_data['activePlayer']
        self.profile.user.email = self.cleaned_data['email']
        self.profile.user.save()
        self.profile.save()
