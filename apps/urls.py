from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import NewPersonViewsets, AllUsersViewsets, RegisterView, TagDetailView, ContactsUsersView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views


router = routers.DefaultRouter()
router.register('person', NewPersonViewsets, basename='person')
router.register('allusers', AllUsersViewsets, basename='allusers')
router.register('contact', ContactsUsersView, basename='contact')

urlpatterns = [
                  path('', include(router.urls)),
                  path('end-points/', views.end_points), # end-points for FrontEnd
                  path("contact/tags/<slug:tag_slug>/", TagDetailView.as_view()),
                  path('auth/', include('djoser.urls')),  # VERIFY BY EMAIL
                  path('auth/', include('djoser.urls.jwt')),  # VERIFY BY EMAIL
                  path('auth/', include('djoser.urls')),
                  path('auth/', include('djoser.urls.jwt')),
                  path('auth/', include('rest_framework.urls')),
                  path('', views.main, name='main'),
                  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
                  path('register/', RegisterView.as_view()),
                  path("ckeditor/", include('ckeditor_uploader.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)