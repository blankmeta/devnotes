from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.hash_functions import get_hash
from api.permissions import NonAuthPostOnly
from api.serializers import ThemeSerializer
from api.serializers import UserSerializer, NoteSerializer
from notes.models import Theme, Note

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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if instance.is_public:
            instance.hash_link = get_hash(str(instance.author) + str(instance.text))
            instance.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class GetNoteByHash(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, hash_link):
        instance = Note.objects.get(hash_link=hash_link)
        serializer = NoteSerializer(instance)
        return Response(serializer.data)
