from django.db import models


class Domain(models.Model):
    domain = models.CharField(max_length=255, primary_key=True)
    description = models.CharField(max_length=255, blank=True)
    aliases = models.IntegerField(default=0)
    mailboxes = models.IntegerField(default=0)
    maxquota = models.BigIntegerField(default=0)
    quota = models.BigIntegerField(default=0)
    transport = models.CharField(max_length=255, blank=True, null=True)
    backupmx = models.BooleanField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    class Meta:
        db_table = "domain"
        managed = False

    def __str__(self):
        return self.domain


class Alias(models.Model):
    address = models.CharField(max_length=255, primary_key=True)
    goto = models.TextField()
    domain = models.CharField(max_length=255)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    class Meta:
        db_table = "alias"
        managed = False

    def __str__(self):
        return self.address


class Mailbox(models.Model):
    username = models.CharField(max_length=255, primary_key=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True)
    maildir = models.CharField(max_length=255)
    quota = models.BigIntegerField(default=0)
    domain = models.CharField(max_length=255)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    class Meta:
        db_table = "mailbox"
        managed = False

    def __str__(self):
        return self.username
