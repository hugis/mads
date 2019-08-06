from django.db import models
from passlib.hash import sha256_crypt


class Domain(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="The name of the domain you want to receive email for.",
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "domains"

    def __str__(self):
        return self.name


class Mailbox(models.Model):
    domain = models.ForeignKey(
        Domain, related_name="mailboxes", on_delete=models.CASCADE
    )
    email = models.CharField(
        max_length=100, unique=True, help_text="The email address of the mail account."
    )
    password = models.CharField(
        max_length=150,
        help_text=(
            "The hashed password of the mail account. It is prepended by the hashing "
            "algorithm. By default it is {SHA256-CRYPT} encrypted. But you may have "
            "legacy users that still use {MD5-CRYPT}. Adding the hashing algorithm "
            "allows you to have different kinds of hashes."
        ),
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "mailboxes"
        verbose_name_plural = "mailboxes"

    def __str__(self):
        return self.email

    def set_password(self, password: str, commit: bool = True) -> "Mailbox":
        self.password = f"{{SHA256-CRYPT}}{sha256_crypt.hash(password)}"
        if commit:
            self.save()
        return self


class Alias(models.Model):
    domain = models.ForeignKey(Domain, related_name="aliases", on_delete=models.CASCADE)
    source = models.CharField(
        max_length=100,
        help_text="The email address that the email was actually sent to.",
    )
    destination = models.CharField(
        max_length=100,
        help_text="The email address that the email should instead be sent to.",
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "alias"
        verbose_name_plural = "aliases"

    def __str__(self):
        return self.source
