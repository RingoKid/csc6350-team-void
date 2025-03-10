from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('projects', views.ProjectViewSet)
router.register('feedbacks', views.FeedbackViewSet)
router.register('ratings', views.RatingViewSet)
router.register('reactions', views.ReactionViewSet)
router.register('collaborations', views.CollaborationViewSet)
router.register('notifications', views.NotificationViewSet)
router.register('searchlogs', views.SearchLogViewSet)
router.register('reports', views.ReportViewSet)


urlpatterns = [
    path('', include(router.urls)),
]