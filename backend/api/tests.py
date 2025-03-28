from django.test import TestCase
from .models import User, Project, Rating, Reaction, Feedback

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
class EditProjectTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            role='Presenter'
        )
        # Create a test project
        self.project = Project.objects.create(
            user=self.user,
            title='Original Title',
            description='Original Description',
            category='Hackathon'
        )
        # Set up API client and log in the user
        self.client = APIClient()
        self.client.login(username='testuser', password='password123')

        # Define updated project data
        self.updated_project_data = {
            'title': 'Updated Title',
            'description': 'Updated Description',
            'category': 'Hackathon',  # Keep the category unchanged
            'user': self.user.id,     # Include the user field if required
        }

    # Test the basic flow: Editing a project
    def test_edit_project_success(self):
        response = self.client.put(f'/api/projects/{self.project.id}/', self.updated_project_data)
        print(response.status_code)  # Print the status code for debugging
        print(response.data)         # Print the response data for debugging
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()  # Refresh the project instance from the database
        self.assertEqual(self.project.title, 'Updated Title')
        self.assertEqual(self.project.description, 'Updated Description')
        self.assertEqual(self.project.category, 'Hackathon')
        self.assertEqual(self.project.user.username, 'testuser')