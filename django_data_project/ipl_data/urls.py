from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='ipl_data-home'),
    path('matches_won/', views.matches_won, name='ipl-data-matches_won'),
    path('matches_played/', views.matches_played, name='ipl-data-matches_played'),
    path('extra_runs/', views.extra_runs, name='ipl-data-extra_runs'),
    path('top_bowlers/', views.top_bowlers, name='ipl-data-top_bowlers'),
    path('top_players/', views.top_players, name='ipl-data-top_players'),
    path('matches_played_chart/', views.matches_played_chart, name='ipl-data-matches_played_chart'),
    path('top_bowlers_chart/', views.top_bowlers_chart, name='ipl-data-top_bowlers_chart'),
    path('extra_runs_chart/', views.extra_runs_chart, name='ipl-data-extra_runs_chart'),
    path('matches_won_chart/', views.matches_won_chart, name='ipl-data-matches_won_chart'),
    path('top_players_chart/',views.top_players_chart, name='ipl-data-top_players_chart')
]
