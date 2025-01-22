from django.contrib.auth.models import User
from django.test import TestCase

from clients.models import Client


class ClientModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_client_str(self):
        client = Client.objects.create(
            name="Empresa Test", nif="12345678A", address="Calle Ejemplo 123",
            city="Sevilla", province="Sevilla", owner=self.user
        )
        self.assertEqual(str(client), "Empresa Test")

    def test_unique_nif_per_owner(self):
        Client.objects.create(
            name="Cliente 1", nif="12345678A", address="Calle A", city="Sevilla", province="Sevilla", owner=self.user
        )
        with self.assertRaises(Exception):
            Client.objects.create(
                name="Cliente 2", nif="12345678A", address="Calle B", city="Sevilla", province="Sevilla",
                owner=self.user
            )

    def test_exists_with_nif_and_owner(self):
        client = Client.objects.create(
            name="Cliente", nif="12345678A", address="Calle Ejemplo", city="Sevilla", province="Sevilla",
            owner=self.user
        )
        self.assertTrue(Client.exists_with_nif_and_owner("12345678A", self.user))
        self.assertFalse(Client.exists_with_nif_and_owner("87654321B", self.user))
