from django.shortcuts import render, HttpResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import NewPersonSerializer, UserSerializer, RegisterSerializer
from .models import NewPerson
from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()
from .serializers import RegisterSerializer, UserSerializer, ContactsUserSerializer

from taggit.models import Tag
from .models import NewPerson, ContactsUser


class ContactsUsersView(viewsets.ModelViewSet):
    serializer_class = ContactsUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if IsAuthenticated:
            id_user = User.objects.get(id=self.request.user.id)
            return ContactsUser.objects.filter(iduserCreator=id_user)


class TagDetailView(generics.ListAPIView):
    serializer_class = ContactsUserSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        if IsAuthenticated:
            id_user = User.objects.get(id=self.request.user.id)
            tag_slug = self.kwargs['tag_slug'].lower()
            tag = Tag.objects.get(slug=tag_slug)
            return ContactsUser.objects.filter(iduserCreator=id_user, tags=tag)


def main(request):
    return HttpResponse("It's work")


class NewPersonViewsets(viewsets.ModelViewSet):
    queryset = NewPerson.objects.all().order_by('first_name')
    serializer_class = NewPersonSerializer
    lookup_field = 'first_name'


class RegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # user = serializer.save()
        return Response({
            # "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "Пользователь успешно создан",
            'data': serializer.data
        })


class AllUsersViewsets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def end_points(request):
    return render(request, 'apps/index.html')
