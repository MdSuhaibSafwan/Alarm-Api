"""alarmapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView, base
from rest_framework.routers import DefaultRouter
# import ddlfs.views
# import ddlfs.api_views
from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from api import views

from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls


router = DefaultRouter()
router.register(r'alarm/current', views.AlarmCurrentViewSet, basename='current')
router.register(r'alarm', views.AlarmViewSet, basename='alarm')
router.register(r'alarm/history', views.AlarmHistoryViewSet, basename='history')
router.register(r'node', views.NodeViewSet, basename='node')
router.register(r'ack', views.AckViewSet, basename='ack')
# router.register(r'alarm/<alarm_id>/ack', views.AlarmSeverityViewSet, basename="sev")


urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/v1/', include(router.urls)),
                  path('api/v1/alarm/<int:alarm_id>/ack/', views.AlarmSeverityViewSet.as_view(), 
                                                                    name="Alarm-Serverity"),
                  path("api/v1/ack/alarm/<id>/", views.AcknowledgementRetrieveAPIView.as_view(), name="Ack-Retrieve"),
                #   path('api/v1/sev/', .as_view(
                #       {'get': 'list', 'post': 'create'}
                #     ), name='detailcreate'),
                  # path('api/auth/', include('djoser.urls.authtoken')),
                  path("api/authentication/", include("rest_framework.urls")),
]
              #     path('ddlfs/', include('ddlfs.urls')),
              #     path('', RedirectView.as_view(url='ddlfs/', permanent=True)),
              # ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

