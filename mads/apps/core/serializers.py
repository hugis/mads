from rest_framework import serializers

from . import models


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Domain
        fields = [
            "domain",
            "description",
            "aliases",
            "mailboxes",
            "maxquota",
            "quota",
            "transport",
            "backupmx",
            "created",
            "modified",
            "active",
        ]


class AliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Alias
        fields = ["address", "goto", "domain", "created", "modified", "active"]
