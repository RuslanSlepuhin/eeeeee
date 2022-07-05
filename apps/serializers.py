from rest_framework import serializers
from .models import NewPerson, ContactsUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer

User = get_user_model()
from taggit.serializers import TagListSerializerField, TaggitSerializer


class ContactsUserSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    # iduserCreator = serializers.SlugRelatedField(slug_field="id", queryset=User.objects.all())
    iduserCreator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ContactsUser
        fields = ('id', 'first_name', 'last_name', 'phone', 'email', 'photo', 'notes', 'iduserCreator', 'tags')
        # extra_kwargs = {"photo": {"read_only": True}}


class NewPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewPerson
        fields = ('id', 'first_name', 'last_name', 'email', 'work_experience')
        lookup_field = 'first_name'
        extra_kwargs = {
            'url': {'lookup_field': 'first_name'}
        }


class RegisterSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        read_only_fields = ['username']
        fields = [
            "email",
            "password",
            "token",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]
        if not password:
            raise serializers.ValidationError({"password": "Введите пароль"})
        user = User(email=email)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



class UserCreateSerializer(serializers.ModelSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['email', 'password']
