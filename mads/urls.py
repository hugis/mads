from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from mads.apps.core import views


router = routers.DefaultRouter()
router.register(r"domains", views.DomainViewSet)
router.register(r"aliases", views.AliasViewSet)
router.register(r"mailboxes", views.MailboxViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("admin/", admin.site.urls),
]
