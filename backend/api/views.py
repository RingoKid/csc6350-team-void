from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

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