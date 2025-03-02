from django.contrib import admin
from .models import Project, Feedback, Rating, Reaction, Collaboration, Notification, SearchLog, Report

admin.site.register(Project)
admin.site.register(Feedback)
admin.site.register(Rating)
admin.site.register(Reaction)
admin.site.register(Collaboration)
admin.site.register(Notification)
admin.site.register(SearchLog)
admin.site.register(Report)