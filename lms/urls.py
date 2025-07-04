"""
URL configuration for pos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
   openapi.Info(
      title="LMS API",
      default_version='v1',
      description="Comprehensive API documentation for the LMS project.",
      terms_of_service="https://www.3pointdev.com/terms/",
      contact=openapi.Contact(email="work.threepointdev@gmail.com"),
      license=openapi.License(name="BSD License", url="https://opensource.org/licenses/BSD-3-Clause"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('userauth.urls')),
    path('api/v1/school/', include('school.urls')),
    path('api/v1/teachers/', include('teachers.urls')),
    path('api/v1/students/', include('students.urls')),
    path('api/v1/quiz/', include('quiz.urls')),
    path('api/v1/', include('v1.urls')),
    path('redoc/', schema_view.with_ui('redoc',cache_timeout=0), name='schema-redoc'),
    path('swagger/', schema_view.with_ui('swagger',cache_timeout=0), name='schema-swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)