from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import User, Project, Feedback, Rating, Reaction, Collaboration, Notification, SearchLog, Report
import random

class Command(BaseCommand):
    help = 'Populate the database with dummy data'

    def handle(self, *args, **kwargs):
        # Create Users
        users = []
        user_names = ['Alice', 'Bob', 'Charlie', 'David', 'Eve']
        for i, name in enumerate(user_names):
            user = User.objects.create_user(
                username=f'{name.lower()}{random.randint(1, 10000)}',
                email=f'{name.lower()}{random.randint(1, 10000)}@example.com',
                password='password',
                role=random.choice(['Presenter', 'Reviewer', 'Admin']),
                institution=f'Institution {i}'
            )
            users.append(user)

        project_titles = [
            'AI-Powered Chatbot',
            'E-Commerce Platform',
            'Social Media Analytics Tool',
            'Online Learning Management System',
            'Healthcare Appointment Scheduler'
        ]

        project_descriptions = [
            'A chatbot that uses AI to provide customer support.',
            'A platform for buying and selling products online.',
            'A tool to analyze social media trends and metrics.',
            'A system to manage online courses and student progress.',
            'An application to schedule and manage healthcare appointments.'
        ]

        # Create Projects
        projects = []
        for i in range(len(project_titles)):
            project = Project.objects.create(
                user=random.choice(users),
                title=project_titles[i],
                description=project_descriptions[i],
                category=random.choice(['Hackathon', 'Class Project', 'Research']),
                created_at=timezone.now(),
                thumbnail=f'https://picsum.photos/seed/{i}/150',
            )
            projects.append(project)

        # Create Feedback
        for i in range(20):
            Feedback.objects.create(
                project=random.choice(projects),
                user=random.choice(users),
                comment=f'Feedback comment {i}',
                created_at=timezone.now()
            )

        # Create Ratings
        for project in projects:
            for _ in range(random.randint(1, 5)):
                Rating.objects.create(
                    project=project,
                    user=random.choice(users),
                    creativity=random.randint(1, 5),
                    technical_skills=random.randint(1, 5),
                    impact=random.randint(1, 5),
                    presentation=random.randint(1, 5),
                    created_at=timezone.now()
                )

        # Create Reactions
        for i in range(20):
            Reaction.objects.create(
                project=random.choice(projects),
                user=random.choice(users),
                reaction_type=random.choice(['Like', 'Love', 'Clap', 'ThumbsUp', 'Star']),
                created_at=timezone.now()
            )

        # Create Collaborations
        for i in range(10):
            Collaboration.objects.create(
                project=random.choice(projects),
                user=random.choice(users),
                status=random.choice(['Pending', 'Accepted', 'Rejected']),
                created_at=timezone.now()
            )

        # Create Notifications
        for i in range(10):
            Notification.objects.create(
                user=random.choice(users),
                message=f'Notification message {i}',
                is_read=random.choice([True, False]),
                created_at=timezone.now()
            )

        # Create Search Logs
        for i in range(10):
            SearchLog.objects.create(
                user=random.choice(users),
                query=f'Search query {i}',
                created_at=timezone.now()
            )

        # Create Reports
        for i in range(5):
            Report.objects.create(
                reported_by=random.choice(users),
                project=random.choice(projects),
                reason=f'Report reason {i}',
                status=random.choice(['Pending', 'Reviewed', 'Resolved']),
                created_at=timezone.now()
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with dummy data')) 