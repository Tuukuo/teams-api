from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from teams.models import Team, Player
from .serializers import TeamSerializer, PlayerSerializer

class TeamListCreate(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def get_queryset(self):
        queryset = Team.objects.all()
        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    def post(self, request, *args, **kwargs):
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Team added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TeamDetail(generics.RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class PlayerListCreate(generics.ListCreateAPIView):
    serializer_class = PlayerSerializer

    def get_queryset(self):
        team_id = self.kwargs['team_id']
        return Player.objects.filter(team_id=team_id)

    def post(self, request, *args, **kwargs):
        team_id = self.kwargs['team_id']
        data = request.data.copy()
        data['team'] = team_id
        serializer = PlayerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Player added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PlayerDetail(generics.RetrieveAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer