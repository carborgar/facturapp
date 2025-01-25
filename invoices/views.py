import os

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from weasyprint import HTML

from clients.models import Client
from .models import Invoice


class InvoiceListView(ListView):
    model = Invoice
    template_name = "invoices/invoice_list.html"
    context_object_name = "invoices"

    def get_queryset(self):
        # Si el usuario es administrador, muestra todas las facturas.
        # if self.request.user.is_admin:
        #     return Invoice.objects.all()
        # Si es facturador, muestra solo sus facturas.
        return Invoice.objects.filter(owner=self.request.user)


class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = "invoices/invoice_detail.html"
    context_object_name = "invoice"


class InvoiceCreateView(CreateView):
    model = Invoice
    fields = ["number", "vat", "client_name", "client_nif", "client_address", "client_city", "client_province"]

    def form_valid(self, form):
        form.instance.owner = self.request.user
        client = Client.objects.get(pk=self.kwargs["client_id"])  # Elige el cliente
        # Copia los datos del cliente
        form.instance.client_name = client.name
        form.instance.client_nif = client.nif
        form.instance.client_address = client.address
        form.instance.client_city = client.city
        form.instance.client_province = client.province
        return super().form_valid(form)


def generate_invoice_pdf(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    static_file_path = os.path.join(base_dir, 'static', 'css', 'invoice.css')
    with open(static_file_path, 'r') as f:
        contenido_css = f.read()

    html_string = render_to_string('invoices/invoice_pdf.html', {'invoice': invoice, 'css': contenido_css})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="factura_{invoice.number}.pdf"'
    HTML(string=html_string).write_pdf(response, stylesheets=[])

    return response
