from django.test import TestCase
from .models import *
class RatingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            role='Presenter'
        )
        self.project = Project.objects.create(
            user=self.user,
            title='Test Project',
            description='This is a test project',
            category='Hackathon'
        )
        self.rating = Rating.objects.create(
            project=self.project,
            user=self.user,
            creativity=5,
            technical_skills=4,
            impact=3,
            presentation=5
        )

    def test_rating_creation(self):
        self.assertEqual(self.rating.creativity, 5)
        self.assertEqual(self.rating.technical_skills, 4)
        self.assertEqual(self.rating.impact, 3)
        self.assertEqual(self.rating.presentation, 5)
        self.assertEqual(self.rating.project.title, 'Test Project')
        self.assertEqual(self.rating.user.username, 'testuser')

class ReactionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            role='Presenter'
        )
        self.project = Project.objects.create(
            user=self.user,
            title='Test Project',
            description='This is a test project',
            category='Hackathon'
        )
        self.reaction = Reaction.objects.create(
            project=self.project,
            user=self.user,
            reaction_type='Like'
        )

    def test_reaction_creation(self):
        self.assertEqual(self.reaction.reaction_type, 'Like')
        self.assertEqual(self.reaction.project.title, 'Test Project')
        self.assertEqual(self.reaction.user.username, 'testuser')