from django.test import TestCase
from clients.forms import ClientForm


class ClientFormTests(TestCase):
    def test_valid_client_form(self):
        form_data = {
            "name": "Cliente Test",
            "nif": "Q3838622C",
            "address": "Calle Ejemplo, 123",
            "city": "Sevilla",
            "province": "Sevilla"
        }
        form = ClientForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_nif_in_client_form(self):
        form_data = {
            "name": "Cliente Test",
            "nif": "INVALIDO",  # NIF no válido
            "address": "Calle Ejemplo, 123",
            "city": "Sevilla",
            "province": "Sevilla"
        }
        form = ClientForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("nif", form.errors)
