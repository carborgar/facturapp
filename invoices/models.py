from django.db import models
from django.conf import settings


class Invoice(models.Model):
    STATUS_CHOICES = [
        ("draft", "Borrador"),
        ("sent", "Enviada"),
        ("paid", "Pagada"),
    ]

    # Datos de la factura
    number = models.CharField(max_length=20, unique=True)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    vat = models.DecimalField(max_digits=5, decimal_places=2)

    # Relación con el usuario
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="invoices"
    )

    # Datos copiados del cliente
    client_name = models.CharField(max_length=255)
    client_nif = models.CharField(max_length=9)
    client_address = models.CharField(max_length=255)
    client_city = models.CharField(max_length=100)
    client_province = models.CharField(max_length=100)

    def __str__(self):
        return f"Factura {self.number} - {self.client_name}"

    def get_subtotal(self):
        return sum(line.get_total() for line in self.lines.all())

    def get_vat(self):
        return self.get_subtotal() * (self.vat / 100)

    def get_total(self):
        return self.get_subtotal() + self.get_vat()


class InvoiceLine(models.Model):
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="lines"
    )
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.description

    def get_total(self):
        return self.quantity * self.unit_price
