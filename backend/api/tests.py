from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import *
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.views import TokenObtainPairView

class BaseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            role='Presenter'
        )


class UserModelTest(BaseTestCase):
    def test_user_creation(self):
        print("--------------------")
        print("Testing user creation...")
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.role, 'Presenter')
        print("User creation test passed!")
     
class RatingModelTest(BaseTestCase):
    def setUp(self):
        super().setUp() 
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

class ReactionModelTest(BaseTestCase):
    def setUp(self):
        super().setUp() 
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
        
class SubmitRatingTestCase(BaseTestCase):
    def setUp(self):
        # Create a test user
        super().setUp() 
        # Create a test project
        self.project = Project.objects.create(
            user=self.user,
            title='Test Project',
            description='This is a test project.',
            category='Hackathon'
        )
        # Set up API client and log in the user
        self.client = APIClient()
        self.client.login(username='testuser', password='password123')

        # Define valid rating data
        self.valid_rating_data = {
            'project': self.project.id,
            'user': self.user.id,
            'creativity': 5,
            'technical_skills': 4,
            'impact': 3,
            'presentation': 5,
        }

    # Test the basic flow: Submitting a valid rating
    def test_submit_rating_success(self):
        response = self.client.post('/api/ratings/', self.valid_rating_data)

                 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rating.objects.count(), 1)
        rating = Rating.objects.first()
        self.assertEqual(rating.creativity, 5)
        self.assertEqual(rating.technical_skills, 4)
        self.assertEqual(rating.impact, 3)
        self.assertEqual(rating.presentation, 5)
        self.assertEqual(rating.project.title, 'Test Project')
        self.assertEqual(rating.user.username, 'testuser')

class ProjectModelTest(BaseTestCase):
    def setUp(self):
        super().setUp() 
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

class FeedbackModelTest(BaseTestCase):
    def setUp(self):
        super().setUp() 
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

class CollaborationModelTest(BaseTestCase):
    def setUp(self):
        super().setUp() 
        self.project = Project.objects.create(
            user=self.user,
            title='Test Project',
            description='This is a test project',
            category='Hackathon'
        )
        self.collaboration = Collaboration.objects.create(
            project=self.project,
            user=self.user,
            status='Pending'
        )

    def test_collaboration_creation(self):
        self.assertEqual(self.collaboration.status, 'Pending')
        self.assertEqual(self.collaboration.project.title, 'Test Project')
        self.assertEqual(self.collaboration.user.username, 'testuser')

class UploadProjectTestCase(BaseTestCase):
    def setUp(self):
        super().setUp() 
        # Set up API client and log in the user
        self.client = APIClient()
        self.client.login(username='testuser', password='password123')

        # Define valid project data
        self.valid_project_data = {
            'title': 'Test Project',
            'description': 'This is a test project.',
            'category': 'Hackathon',
            'video_url': 'https://example.com/video.mp4',
            'user': self.user.id,  # Include the user field
        }

    # Test the basic flow: Uploading a valid project
    def test_upload_project_success(self):
        response = self.client.post('/api/projects/', self.valid_project_data)
          
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
        project = Project.objects.first()
        self.assertEqual(project.title, 'Test Project')
        self.assertEqual(project.description, 'This is a test project.')
        self.assertEqual(project.category, 'Hackathon')
        self.assertEqual(project.video_url, 'https://example.com/video.mp4')
        self.assertEqual(project.user.username, 'testuser')

class EditProjectTestCase(BaseTestCase):
    def setUp(self):
        # Create a test user
        super().setUp() 
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

                 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()  # Refresh the project instance from the database
        self.assertEqual(self.project.title, 'Updated Title')
        self.assertEqual(self.project.description, 'Updated Description')
        self.assertEqual(self.project.category, 'Hackathon')
        self.assertEqual(self.project.user.username, 'testuser')
        self.assertEqual(self.project.user.username, 'testuser')

class SubmitRatingTestCase(BaseTestCase):
    def setUp(self):
        # Create a test user
        super().setUp() 
        # Create a test project
        self.project = Project.objects.create(
            user=self.user,
            title='Test Project',
            description='This is a test project.',
            category='Hackathon'
        )
        # Set up API client and log in the user
        self.client = APIClient()
        self.client.login(username='testuser', password='password123')

        # Define valid rating data
        self.valid_rating_data = {
            'project': self.project.id,
            'user': self.user.id,
            'creativity': 5,
            'technical_skills': 4,
            'impact': 3,
            'presentation': 5,
        }

    # Test the basic flow: Submitting a valid rating
    def test_submit_rating_success(self):
        response = self.client.post('/api/ratings/', self.valid_rating_data)

                 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rating.objects.count(), 1)
        rating = Rating.objects.first()
        self.assertEqual(rating.creativity, 5)
        self.assertEqual(rating.technical_skills, 4)
        self.assertEqual(rating.impact, 3)
        self.assertEqual(rating.presentation, 5)
        self.assertEqual(rating.project.title, 'Test Project')
        self.assertEqual(rating.user.username, 'testuser')

class NotificationModelTest(BaseTestCase):
    def setUp(self):
      super().setUp() 
      self.notification = Notification.objects.create(
            user=self.user,
            message='This is a test notification',
            is_read=False
        )

    def test_notification_creation(self):
        self.assertEqual(self.notification.message, 'This is a test notification')
        self.assertEqual(self.notification.is_read, False)
        self.assertEqual(self.notification.user.username, 'testuser')
        
class ProjectSearchTestCase(BaseTestCase):
    def setUp(self):
        super().setUp() 
        self.project1 = Project.objects.create(
            user=self.user,
            title='Hackathon Project',
            description='A project for a hackathon',
            category='Hackathon'
        )
        self.project2 = Project.objects.create(
            user=self.user,
            title='AI Research',
            description='A project about artificial intelligence',
            category='Research'
        )
        self.project3 = Project.objects.create(
            user=self.user,
            title='Web Development',
            description='A project about building websites',
            category='Development'
        )
        self.client = APIClient()

    def test_search_projects(self):
        print("--------------------")
        print("Testing search project...")
        response = self.client.get('/api/projects/search/?q=Hackathon')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Hackathon Project')
        print("Search project test passed!")

class UploadProjectTestCase(BaseTestCase):
    def setUp(self):
        # Create a test user
        super().setUp() 
        # Set up API client and log in the user
        self.client = APIClient()
        self.client.login(username='testuser', password='password123')

        # Define valid project data
        self.valid_project_data = {
            'title': 'Test Project',
            'description': 'This is a test project.',
            'category': 'Hackathon',
            'video_url': 'https://example.com/video.mp4',
            'user': self.user.id,  # Include the user field
        }

    # Test the basic flow: Uploading a valid project
    def test_upload_project_success(self):
        response = self.client.post('/api/projects/', self.valid_project_data)
          
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
        project = Project.objects.first()
        self.assertEqual(project.title, 'Test Project')
        self.assertEqual(project.description, 'This is a test project.')
        self.assertEqual(project.category, 'Hackathon')
        self.assertEqual(project.video_url, 'https://example.com/video.mp4')
        self.assertEqual(project.user.username, 'testuser')

class SearchLogModelTest(BaseTestCase):
    def setUp(self):
        super().setUp() 
        self.search_log = SearchLog.objects.create(
            user=self.user,
            query='test query'
        )

    def test_search_log_creation(self):
        self.assertEqual(self.search_log.query, 'test query')
        self.assertEqual(self.search_log.user.username, 'testuser')

class ReportModelTest(BaseTestCase):
    def setUp(self):
        super().setUp() 
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
        self.report = Report.objects.create(
            reported_by=self.user,
            project=self.project,
            feedback=self.feedback,
            reason='This is a test report',
            status='Pending'
        )

    def test_report_creation(self):
        self.assertEqual(self.report.reason, 'This is a test report')
        self.assertEqual(self.report.status, 'Pending')
        self.assertEqual(self.report.reported_by.username, 'testuser')
        self.assertEqual(self.report.project.title, 'Test Project')
        self.assertEqual(self.report.feedback.comment, 'This is a test feedback')

class UserLoginTestCase(BaseTestCase):
    def setUp(self):
    # Create a test user
        super().setUp() 
        # Set up APIRequestFactory
        self.factory = APIRequestFactory()

    # Test the basic flow: User logs in successfully
    def test_user_login_success(self):
        # Define login credentials
        login_data = {
            'username': 'testuser',
            'password': 'password123'
        }
        # Create a POST request using APIRequestFactory
        request = self.factory.post('/token/', login_data)
        # Call the TokenObtainPairView directly
        view = TokenObtainPairView.as_view()
        response = view(request)
        # Assert the response status code is 200 OK
        self.assertEqual(response.status_code, 200)
        # Assert the response contains access and refresh tokens
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

class UserSignUpTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_signup_success(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
            "confirm_password": "password123",
            "role": "Presenter",
            "institution": "Test Institution"
        }
        response = self.client.post('/api/auth/signup/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "User registered successfully!")

    def test_user_signup_password_mismatch(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
            "confirm_password": "wrongpassword",
            "role": "Presenter"
        }
        response = self.client.post('/api/auth/signup/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Passwords do not match.", str(response.data))