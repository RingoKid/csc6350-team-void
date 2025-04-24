from django.contrib import admin
from django import forms
from django.db.models import F
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import get_object_or_404
import logging
from .models import Project, Feedback, Rating, Reaction, Collaboration, Notification, SearchLog, User, ReportedFeedback

logger = logging.getLogger(__name__)

class ProjectAdminForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        # Store the original thumbnail value
        if self.instance and self.instance.pk:
            self.original_thumbnail = self.instance.thumbnail
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.instance and self.instance.pk:
            # If only thumbnail has changed
            if 'thumbnail' in self.changed_data and len(self.changed_data) == 1:
                logger.info(f"Only thumbnail changed from {self.original_thumbnail} to {instance.thumbnail}")
                # Update only the thumbnail field
                Project.objects.filter(pk=self.instance.pk).update(thumbnail=instance.thumbnail)
                return self.instance
        if commit:
            instance.save()
        return instance

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description')
    raw_id_fields = ('user',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('comment',)
    raw_id_fields = ('user', 'project')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    raw_id_fields = ('user', 'project')

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'reaction_type', 'created_at')
    list_filter = ('reaction_type', 'created_at')
    raw_id_fields = ('user', 'project')

@admin.register(Collaboration)
class CollaborationAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    raw_id_fields = ('user', 'project')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('message',)
    raw_id_fields = ('user',)

@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'query', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('query',)
    raw_id_fields = ('user',)

@admin.register(ReportedFeedback)
class ReportedFeedbackAdmin(admin.ModelAdmin):
    list_display = ('feedback', 'reporter', 'is_resolved', 'created_at')
    list_filter = ('is_resolved', 'created_at')
    search_fields = ('reason',)
    raw_id_fields = ('feedback', 'reporter', 'resolved_by')
