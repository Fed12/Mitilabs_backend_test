
from django.contrib import admin
from django.urls import path
from myapp import views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static
from .settings import AWS_S3_CUSTOM_DOMAIN

from django.views.generic import TemplateView

urlpatterns = [
    path('docs/', TemplateView.as_view(
        template_name='docs.html',
        extra_context={'schema_url':'api_schema'}
        ), name='swagger-ui'),
]

MEDIA_URL = AWS_S3_CUSTOM_DOMAIN + '/files'

from rest_framework_swagger.views import get_swagger_view
from django.urls import re_path

schema_view = get_swagger_view(title='Pastebin API')

from django.views.generic import RedirectView
from django.urls import path
from rest_framework import permissions

# from rest_framework.schemas import get_schema_view
from drf_yasg.views import get_schema_view

from drf_yasg import openapi

from .settings import DEBUG



# schema_url = {} if DEBUG else {'url': 'https://domain.com/'}

#schema_view = get_swagger_view(title='Pastebin API')

from rest_framework_swagger.views import get_swagger_view

schema_view = get_schema_view(
    openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # path('api_schema', get_schema_view(title='API Schema', description='example'), name ='api_schema'),
    path('admin/', admin.site.urls),
    path('visualize/', views.Visualize.as_view()),
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]

