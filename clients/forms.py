from localflavor.es.forms import ESIdentityCardNumberField

from core.forms import NoPlaceholderModelForm
from .models import Client


class ClientForm(NoPlaceholderModelForm):
    nif = ESIdentityCardNumberField(label="NIF/CIF")

    class Meta:
        model = Client
        fields = ['name', 'nif', 'address', 'city', 'province']
        labels = {
            'name': 'Nombre',
            'address': 'Dirección',
            'city': 'Ciudad',
            'province': 'Provincia',
        }
        help_texts = {
            'name': 'Nombre completo o razón social',
            'address': 'Ejemplo: C/Ejemplo, 123, 4ºA',
        }
