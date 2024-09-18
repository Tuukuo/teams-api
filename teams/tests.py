from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from teams.models import Team, Player

class TeamTests(APITestCase):
    def setUp(self):
        # Create a valid image in memory for the logo
        logo_image = BytesIO()
        img = Image.new('RGB', (100, 100), color='red')
        img.save(logo_image, format='JPEG')
        logo_image.seek(0)  # Reset file pointer to the beginning

        self.logo = SimpleUploadedFile("logo.jpg", logo_image.read(), content_type="image/jpeg")

        self.team = Team.objects.create(
            name="Test Team",
            sport="Football",
            number_of_players=11,
            logo=self.logo
        )
        self.team_url = reverse('team-list-create')
        self.team_detail_url = reverse('team-detail', kwargs={'pk': self.team.id})

    def test_create_team(self):
        # Create a valid image in memory for the new team logo
        new_logo_image = BytesIO()
        img = Image.new('RGB', (100, 100), color='blue')
        img.save(new_logo_image, format='JPEG')
        new_logo_image.seek(0)  # Reset file pointer to the beginning

        logo = SimpleUploadedFile("new_logo.jpg", new_logo_image.read(), content_type="image/jpeg")
        
        data = {
            'name': 'New Team',
            'sport': 'Basketball',
            'number_of_players': 5,
            'logo': logo
        }
        response = self.client.post(self.team_url, data, format='multipart')
        print(response.data)  # Debug line
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Team added successfully')

    def test_get_team_list(self):
        response = self.client.get(self.team_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ensure there is one team

    def test_get_team_detail(self):
        response = self.client.get(self.team_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.team.name)

class PlayerTests(APITestCase):
    def setUp(self):
        # Create a valid image in memory for the player's profile picture
        profile_picture_image = BytesIO()
        img = Image.new('RGB', (100, 100), color='green')
        img.save(profile_picture_image, format='JPEG')
        profile_picture_image.seek(0)  # Reset file pointer to the beginning

        self.profile_picture = SimpleUploadedFile("player.jpg", profile_picture_image.read(), content_type="image/jpeg")
        
        self.team = Team.objects.create(
            name="Test Team",
            sport="Football",
            number_of_players=11,
            logo=self.profile_picture  # Use the same file for the logo
        )
        self.player = Player.objects.create(
            team=self.team,
            name="Test Player",
            profile_picture=self.profile_picture,
            position="Forward",
            date_of_birth="1990-01-01"
        )
        self.player_url = reverse('player-list-create', kwargs={'team_id': self.team.id})
        self.player_detail_url = reverse('player-detail', kwargs={'pk': self.player.id})

    def test_create_player(self):
        # Create a valid image in memory for the new player's profile picture
        new_profile_picture_image = BytesIO()
        img = Image.new('RGB', (100, 100), color='yellow')
        img.save(new_profile_picture_image, format='JPEG')
        new_profile_picture_image.seek(0)  # Reset file pointer to the beginning

        profile_picture = SimpleUploadedFile("new_player.jpg", new_profile_picture_image.read(), content_type="image/jpeg")
        
        data = {
            'name': 'New Player',
            'profile_picture': profile_picture,
            'position': 'Midfielder',
            'date_of_birth': '1992-02-02'
        }
        response = self.client.post(self.player_url, data, format='multipart')
        print(response.data)  # Debug line
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Player added successfully')

    def test_get_player_list(self):
        response = self.client.get(self.player_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ensure there is one player

    def test_get_player_detail(self):
        response = self.client.get(self.player_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.player.name)