from django.urls import path, include
from rest_framework import routers

from api import views
from api.views import UserViewSet, ThemeViewSet, NoteViewSet

router = routers.DefaultRouter()
router.register(r'themes', ThemeViewSet, basename='themes')
router.register(r'notes', NoteViewSet, basename='recent_notes')
router.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/users/me/', views.GetCurrentUser.as_view()),
    path('v1/<str:hash_link>/', views.GetNoteByHash.as_view()),
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
