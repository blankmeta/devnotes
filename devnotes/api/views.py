from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from api.permissions import NonAuthPostOnly
from api.serializers import UserSerializer, NoteSerializer
from django.contrib.auth import get_user_model
from rest_framework import viewsets, filters

from notes.models import Theme, Note

from api.serializers import ThemeSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (NonAuthPostOnly,)


class ThemeViewSet(viewsets.ModelViewSet):
    serializer_class = ThemeSerializer

    def get_queryset(self):
        return Theme.objects.prefetch_related('author').filter(
            author=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        instance.author.remove(self.request.user)
        Note.objects.select_related(
            'author').select_related(
            'theme').filter(
            author=self.request.user, theme=instance).delete()


class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer

    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ('pub_date', 'theme__slug')
    search_fields = ('title',)

    def get_queryset(self):
        return Note.objects.select_related('author').filter(
            author=self.request.user.id)

    def perform_create(self, serializer):
        theme = get_object_or_404(Theme, slug=self.request.data['theme'],
                                  author=self.request.user)
        serializer.save(author=self.request.user, theme=theme)
