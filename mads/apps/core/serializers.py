from rest_framework import serializers

from . import models


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Domain
        fields = ["name", "created", "modified", "active"]


class MailboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Mailbox
        fields = ["domain", "email", "password", "created", "modified", "active"]


class AliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Alias
        fields = ["domain", "source", "destination", "created", "modified", "active"]
