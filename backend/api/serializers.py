from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Feedback
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['creativity', 'technical_skills', 'impact', 'presentation', 'user']

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

class ProjectSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    feedbacks = FeedbackSerializer(many=True, read_only=True, source='feedback_set')

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'thumbnail', 'category', 'video_url', 'user', 'username', 'feedbacks']

from rest_framework import serializers
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'role', 'profile_picture', 'institution']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm_password before saving
        role = validated_data.pop('role', 'Presenter') 
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'Presenter'),  # Default to 'Presenter' if not provided
            profile_picture=validated_data.get('profile_picture'),
            institution=validated_data.get('institution')
        )
        return user