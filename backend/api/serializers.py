from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Feedback
        fields = ['id', 'project', 'user', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Rating
        fields = ['id', 'project', 'user', 'rating', 'created_at']
        read_only_fields = ['user']

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

class ProjectSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    average_rating = serializers.FloatField(read_only=True)
    rating_count = serializers.IntegerField(read_only=True)
    user_rating = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'category', 'thumbnail', 
                 'created_at', 'updated_at', 'user', 'average_rating', 
                 'rating_count', 'user_rating']
        read_only_fields = ['user']

    def get_user_rating(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                rating = Rating.objects.get(project=obj, user=request.user)
                return rating.rating
            except Rating.DoesNotExist:
                pass
        return None

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

class ReportedFeedbackSerializer(serializers.ModelSerializer):
    feedback = FeedbackSerializer(read_only=True)
    reporter = serializers.ReadOnlyField(source='reporter.username')
    resolved_by = serializers.ReadOnlyField(source='resolved_by.username', allow_null=True)
    feedback_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ReportedFeedback
        fields = ['id', 'feedback', 'feedback_id', 'reporter', 'reason', 'created_at', 'is_resolved', 'resolved_by', 'resolved_at']
        read_only_fields = ['id', 'created_at', 'resolved_by', 'resolved_at']
        depth = 1

    def create(self, validated_data):
        feedback_id = validated_data.pop('feedback_id')
        feedback = Feedback.objects.get(id=feedback_id)
        return ReportedFeedback.objects.create(feedback=feedback, **validated_data)

class ReportedProjectSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    reporter = serializers.ReadOnlyField(source='reporter.username')
    resolved_by = serializers.ReadOnlyField(source='resolved_by.username', allow_null=True)
    project_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ReportedProject
        fields = ['id', 'project', 'project_id', 'reporter', 'reason', 'created_at', 'is_resolved', 'resolved_by', 'resolved_at']
        read_only_fields = ['id', 'created_at', 'resolved_by', 'resolved_at']
        depth = 1

    def create(self, validated_data):
        project_id = validated_data.pop('project_id')
        project = Project.objects.get(id=project_id)
        return ReportedProject.objects.create(project=project, **validated_data)