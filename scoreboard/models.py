from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Challenge(models.Model):
    contender = models.ForeignKey(User, on_delete = models.CASCADE, related_name="challenge_contender")
    challengee = models.ForeignKey(User, on_delete = models.CASCADE, related_name="challenge_challengee")
    challenge_date= models.DateTimeField()
    expiration_date = models.DateTimeField(null = True)
    contender_score = models.IntegerField(null=True, blank=True)
    challengee_score = models.IntegerField(null=True, blank = True)
    challenge_open = models.BooleanField(default = True)
    game_reported = models.BooleanField()
    game_date = models.DateTimeField(null=True, blank = True)

    def __str__(self):
        result = ''
        if self.challenge_open:
            result = ' not yet played'
        else:
            result = str(self.contender_score) + ':' + str(self.challengee_score) + " played on " + str(self.game_date)
                
        return self.contender.username + " vs. " + self.challengee.username + ": "  + result

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activePlayer = models.BooleanField(default = True)
    points = models.IntegerField(default = 0)
    trend = models.IntegerField(default = 0)

    def __str__(self):
        return self.user.username

class GameResultValidation(models.Model):
    token = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    report_date = models.DateTimeField()
    expiration_date = models.DateTimeField(null=True)
    game = models.OneToOneField(Challenge, on_delete=models.CASCADE)
