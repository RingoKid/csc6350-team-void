from rest_framework import serializers
from .models import Project, Feedback, Rating, Reaction, Collaboration, Notification, SearchLog, Report, User

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Project
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Feedback
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Rating
        fields = '__all__'

class ReactionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Reaction
        fields = '__all__'

class CollaborationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Collaboration
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Notification
        fields = '__all__'

class SearchLogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SearchLog
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Report
        fields = '__all__'
