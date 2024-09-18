
# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Team, Player

def team_list(request):
    teams = Team.objects.all()
    return render(request, 'teams/team_list.html', {'teams': teams})

def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    return render(request, 'teams/team_detail.html', {'team': team})

def player_detail(request, pk):
    player = get_object_or_404(Player, pk=pk)
    return render(request, 'teams/player_detail.html', {'player':player})
