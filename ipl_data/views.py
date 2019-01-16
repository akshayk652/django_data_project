from django.shortcuts import render
from .models import Matches, Deliveries
from django.db.models import Count, Sum, ExpressionWrapper, F, Q, FloatField
from django.http import JsonResponse
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@cache_page(CACHE_TTL)
def home(request):
    return render(request, 'ipl_data/home.html')


@cache_page(CACHE_TTL)
def matches_played(request):
    matches_played = Matches.objects.values('season').annotate(count=Count('season'))
    context = list(matches_played)
    return JsonResponse(context, safe=False)


@cache_page(CACHE_TTL)
def matches_won(request):
    matches_won = Matches.objects.values('season','winner').annotate(count=Count('winner'))
    context = list(matches_won)
    return JsonResponse(context, safe=False)


@cache_page(CACHE_TTL)
def extra_runs(request):
    extra_runs = Deliveries.objects.values('bowling_team').annotate(Sum('extra_runs')).filter(match__season=2016)
    context = list(extra_runs)
    return JsonResponse(context, safe=False)


@cache_page(CACHE_TTL)
def top_bowlers(request):
    top_bowlers = Deliveries.objects.filter(match__season='2015').values('bowler').annotate(r=Sum('total_runs'),br=Sum('bye_runs'),lbr=Sum('legbye_runs')).annotate(economy=ExpressionWrapper((F('r')-F('br')-F('lbr'))/(Count('ball',filter=Q(noball_runs=0)&Q(wide_runs=0))/6),output_field=FloatField())).order_by('economy')[:10]
    context = list(top_bowlers)
    return JsonResponse(context, safe=False)


@cache_page(CACHE_TTL)
def top_players(request):
    if request.method == 'POST':
        season = request.POST.get('year', None)
        top_players = Matches.objects.filter(season=int(season)).values('player_of_match').annotate(no_of_titles=Count('player_of_match')).order_by('-no_of_titles')[:10]
        context = list(top_players)
        return JsonResponse(context, safe=False)
    else:
        return render(request, 'ipl_data/top_players_menu.html')



@cache_page(CACHE_TTL)
def matches_played_chart(request):
    matches_played = Matches.objects.values('season').annotate(count=Count('season')).order_by('season')
    return render(request, 'ipl_data/matches_played_chart.html', {'matches_played': matches_played})


@cache_page(CACHE_TTL)
def top_bowlers_chart(request):
    top_bowlers = Deliveries.objects.filter(match__season='2015').values('bowler').annotate(r=Sum('total_runs'),br=Sum('bye_runs'),lbr=Sum('legbye_runs')).annotate(economy=ExpressionWrapper((F('r')-F('br')-F('lbr'))/(Count('ball',filter=Q(noball_runs=0)&Q(wide_runs=0))/6),output_field=FloatField())).order_by('economy')[:10]
    return render(request, 'ipl_data/top_bowlers_chart.html', {'top_bowlers': top_bowlers})


@cache_page(CACHE_TTL)
def extra_runs_chart(request):
    extra_runs = Deliveries.objects.values('bowling_team').annotate(runs=Sum('extra_runs')).filter(match__season=2016)
    return render(request, 'ipl_data/extra_runs_chart.html', {'extra_runs': extra_runs})


@cache_page(CACHE_TTL)
def matches_won_chart(request):
    matches_won = list(Matches.objects.values('season','winner').annotate(count=Count('winner')).order_by('season','winner'))
    seasons = []
    teams = []
    team_wins = {}

    for match in matches_won:
        if match['winner']:
            if match['season'] not in seasons:
                seasons.append(match['season'])
            if match['winner'] not in teams:
                teams.append(match['winner'])   

    year = 0
    for match in matches_won:
        if match['winner']:
            if year != match['season']:
                if len(team_wins) != 0:
                    for team in teams:
                        if team not in teams_played:
                            if team in team_wins.keys():
                                team_wins[team].append(0)
                            else:
                                team_wins[team] = [0]
                year = match['season']
                teams_played = set()
            else:
                teams_played.add(match['winner'])

            if match['winner'] not in team_wins.keys():
                team_wins[match['winner']] = []
            teams_played.add(match['winner'])
            team_wins[match['winner']].append(int(match['count']))
        
    return render(request, 'ipl_data/matches_won_chart.html', {'seasons': seasons,'team_wins': team_wins})


@cache_page(CACHE_TTL)
def top_players_chart(request):
    if request.method == 'POST':
        season = request.POST.get('year', None)
        top_players = Matches.objects.filter(season=int(season)).values('player_of_match').annotate(no_of_titles=Count('player_of_match')).order_by('-no_of_titles')[:10]
        print(top_players,request.POST)
        return render(request, 'ipl_data/top_players_chart.html', {'top_players' : top_players})
    else:
        return render(request, 'ipl_data/top_players_menu.html')