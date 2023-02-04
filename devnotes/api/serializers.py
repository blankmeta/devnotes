from django.contrib.auth import get_user_model
from rest_framework import serializers

from notes.models import Theme, Note

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        return user

    class Meta:
        ref_name = 'User1'

        fields = '__all__'
        model = User


class ThemeSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    slug = serializers.SlugField(required=False, read_only=True)

    def create(self, validated_data):
        theme, created = Theme.objects.get_or_create(
            title=validated_data.get('title'))
        theme.author.add(self.context['request'].user)
        return theme

    def validate(self, data):
        if len(Theme.objects.filter(title=data.get('title'))) != 0:
            theme = Theme.objects.get(title=data.get('title'))
            if theme in self.context['request'].user.themes.all():
                raise serializers.ValidationError(
                    'You already have this theme')
        return data

    class Meta:
        fields = '__all__'
        model = Theme


class NoteSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        required=False,
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault())
    theme = serializers.SlugRelatedField(slug_field='slug',
                                         queryset=Theme.objects.all())

    class Meta:
        fields = '__all__'
        model = Note
