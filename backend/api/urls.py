from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ProjectSearchView


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
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('projects/search/', ProjectSearchView.as_view(), name='project_search'),
    path('', include(router.urls)),
]