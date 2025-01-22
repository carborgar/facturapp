from django.conf import settings
from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=255)
    nif = models.CharField(max_length=9)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="clients")

    class Meta:
        unique_together = ('nif', 'owner')  # Ensures unique NIF per owner

    def __str__(self):
        return self.name

    @staticmethod
    def exists_with_nif_and_owner(nif, owner, exclude_pk=None):
        """
        Verifica si existe un cliente con el mismo NIF y dueño, excluyendo un PK opcional.
        """
        query = Client.objects.filter(nif=nif, owner=owner)
        if exclude_pk:
            query = query.exclude(pk=exclude_pk)
        return query.exists()
