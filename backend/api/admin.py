from django.contrib import admin
from django import forms
from django.db.models import F
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import get_object_or_404
import logging
from .models import Project, Feedback, Rating, Reaction, Collaboration, Notification, SearchLog, Report, User

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
    list_display = ('username', 'email', 'role', 'institution', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'institution')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('username',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    readonly_fields = ('created_at', 'updated_at', 'user')
    ordering = ('-created_at',)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields
        return ('created_at', 'updated_at')  # allow user selection for new objects

    def save_model(self, request, obj, form, change):
        if not change:  # If this is a new object
            obj.user = request.user
            obj.save()

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:project_id>/update-thumbnail/',
                self.admin_site.admin_view(self.update_thumbnail),
                name='project-update-thumbnail',
            ),
        ]
        return custom_urls + urls

    def update_thumbnail(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        if request.method == 'POST':
            new_thumbnail = request.POST.get('thumbnail')
            if new_thumbnail:
                try:
                    # Use raw SQL to update only the thumbnail field
                    from django.db import connection
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "UPDATE api_project SET thumbnail = %s WHERE id = %s",
                            [new_thumbnail, project_id]
                        )
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
                except Exception as e:
                    logger.error(f"Error updating thumbnail: {str(e)}")
                    raise
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('comment', 'project__title', 'user__username')
    readonly_fields = ('created_at', 'project', 'user')
    raw_id_fields = ('project', 'user')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('project__title', 'user__username')
    readonly_fields = ('created_at',)
    raw_id_fields = ('project', 'user')

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('project', 'user')
        return self.readonly_fields

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'reaction_type', 'created_at')
    list_filter = ('reaction_type', 'created_at')
    search_fields = ('project__title', 'user__username')
    readonly_fields = ('created_at', 'project', 'user')
    raw_id_fields = ('project', 'user')

@admin.register(Collaboration)
class CollaborationAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('project__title', 'user__username')
    readonly_fields = ('created_at', 'project', 'user')
    raw_id_fields = ('project', 'user')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message')
    readonly_fields = ('created_at', 'user')
    raw_id_fields = ('user',)

@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'query', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'query')
    readonly_fields = ('created_at', 'user')
    raw_id_fields = ('user',)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('reported_by', 'project', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('reported_by__username', 'project__title', 'reason')
    readonly_fields = ('created_at', 'reported_by', 'project', 'feedback')
    raw_id_fields = ('project', 'feedback', 'reported_by')

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields
        return ('created_at',)  # allow selection for new objects
