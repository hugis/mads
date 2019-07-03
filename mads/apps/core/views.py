from rest_framework import viewsets

from . import models, serializers


class DomainViewSet(viewsets.ModelViewSet):
    """API endpoint that allows domains to be viewed or edited."""

    queryset = models.Domain.objects.all().order_by("-created")
    serializer_class = serializers.DomainSerializer
