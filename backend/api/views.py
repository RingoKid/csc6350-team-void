from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly, BasePermission
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

class IsOwnerOrSuperuser(BasePermission):
    """
    Custom permission to only allow owners of a project or superusers to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Superusers can edit any project
        if request.user.is_superuser:
            return True

        # Write permissions are only allowed to the project owner
        return obj.user == request.user

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrSuperuser]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrSuperuser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def rate(self, request, pk=None):
        project = self.get_object()
        rating_value = request.data.get('rating')
        
        if not rating_value or not isinstance(rating_value, (int, float)) or not (1 <= rating_value <= 5):
            return Response(
                {'error': 'Please provide a valid rating between 1 and 5'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update or create the rating
        rating, created = Rating.objects.update_or_create(
            project=project,
            user=request.user,
            defaults={'rating': rating_value}
        )

        serializer = RatingSerializer(rating)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def ratings(self, request, pk=None):
        project = self.get_object()
        ratings = project.ratings.all()
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data)

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer

class CollaborationViewSet(viewsets.ModelViewSet):
    queryset = Collaboration.objects.all()
    serializer_class = CollaborationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class SearchLogViewSet(viewsets.ModelViewSet):
    queryset = SearchLog.objects.all()
    serializer_class = SearchLogSerializer

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    
class ProjectSearchView(APIView):
    def get(self, request):
        # Get the search keyword from the query parameters
        keyword = request.query_params.get('q', '')

        # Filter projects based on the keyword (search in title and description)
        projects = Project.objects.filter(
            title__icontains=keyword
        ) | Project.objects.filter(
            description__icontains=keyword
        )

        # Serialize the filtered projects
        serializer = ProjectSerializer(projects, many=True)

        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectFeedbackView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, project_id):
        feedbacks = Feedback.objects.filter(project_id=project_id)
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserProjectsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Get projects where the current user is the user
        projects = Project.objects.filter(user=request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)