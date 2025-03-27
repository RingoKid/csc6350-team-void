from django.test import TestCase
from .models import *

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            role='Presenter'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.role, 'Presenter')
        
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
        
class ProjectModelTest(TestCase):
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

    def test_project_creation(self):
        self.assertEqual(self.project.title, 'Test Project')
        self.assertEqual(self.project.description, 'This is a test project')
        self.assertEqual(self.project.category, 'Hackathon')
        self.assertEqual(self.project.user.username, 'testuser')

class FeedbackModelTest(TestCase):
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
        self.feedback = Feedback.objects.create(
            project=self.project,
            user=self.user,
            comment='This is a test feedback'
        )

    def test_feedback_creation(self):
        self.assertEqual(self.feedback.comment, 'This is a test feedback')
        self.assertEqual(self.feedback.project.title, 'Test Project')
        self.assertEqual(self.feedback.user.username, 'testuser')