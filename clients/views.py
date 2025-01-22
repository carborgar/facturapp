from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.views.generic.edit import CreateView

from .forms import ClientForm
from .models import Client


@login_required
def listar_clients(request):
    clients = Client.objects.filter(owner=request.user)

    return render(request, 'clients/list.html', {'clients': clients})


class ClientUpsertView(LoginRequiredMixin, CreateView, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('list_clients')

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        if pk:
            messages.info(self.request, 'Modificar un cliente no afecta a las facturas pasadas.')
            return get_object_or_404(Client, pk=pk, owner=self.request.user)
        return None

    def form_valid(self, form):
        # Asociamos el cliente al usuario autenticado
        form.instance.owner = self.request.user

        # Validación personalizada de NIF
        nif = form.cleaned_data['nif']
        exclude_pk = self.get_object().pk if self.get_object() else None

        if Client.exists_with_nif_and_owner(nif, self.request.user, exclude_pk):
            form.add_error('nif', 'Ya existe un cliente con este NIF en tu cartera.')
            return self.form_invalid(form)

        messages.success(self.request, 'Cliente guardado con éxito.')

        return super().form_valid(form)
