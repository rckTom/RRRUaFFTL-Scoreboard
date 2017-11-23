from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^challenge', views.challenge, name = 'challenge'),
    url(r'^add_challenge_result',views.add_challenge_result, name='add_challenge_result'),
    url(r'^my_challenges',views.my_challenges,name='my_challenges'),
    url(r'^thanks', views.thanks, name='thanks'),
    url(r'^ranking', views.ranking, name='ranking'),
    url(r'^points_overview',views.points_overview, name='points_overview'),
    url(r'^statistics',views.statistics, name='statistics'),
    url(r'^awards',views.awards, name = 'awards'),
    url(r'^all_games',views.all_games,name='all_games'),
    url(r'^report_confirmation',views.ReportConfirmation.as_view(),name='report_confirmation'),
    url(r'^profile',views.profile,name="profile")
    ]
