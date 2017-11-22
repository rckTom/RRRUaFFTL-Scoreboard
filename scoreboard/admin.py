from django.contrib import admin
from . import models

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','activePlayer','points')

class GameAdmin(admin.ModelAdmin):
    pass

class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('contender','challengee','challenge_open','challenge_date','game_date')

class TokenAdmin(admin.ModelAdmin):
    list_display = ['token']

admin.site.register(models.Challenge, ChallengeAdmin)
admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.GameResultValidation,TokenAdmin)