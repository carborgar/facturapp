from django.urls import path

from . import views

urlpatterns = [
    path("", views.InvoiceListView.as_view(), name="invoice_list"),  # Listado de facturas
    path("new/", views.InvoiceCreateView.as_view(), name="invoice_create"),  # Nueva factura
    path("<int:pk>/", views.InvoiceDetailView.as_view(), name="invoice_detail"),  # Detalles de una factura
    path("<int:pk>/pdf/", views.generate_invoice_pdf, name="invoice_pdf"),  # Generar PDF
]
