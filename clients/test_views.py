from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Client

User = get_user_model()


class ClientViewsTestCase(TestCase):
    def setUp(self):
        """
        Configuración inicial para las pruebas. Creamos un usuario de prueba y lo autenticamos.
        """
        # Crear un usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Crear clientes asociados al usuario
        self.client1 = Client.objects.create(
            name='Cliente 1',
            nif='24250524Z',
            address='Calle 1, 123',
            city='Ciudad 1',
            province='Provincia 1',
            owner=self.user
        )
        self.client2 = Client.objects.create(
            name='Cliente 2',
            nif='A61022745',
            address='Calle 2, 234',
            city='Ciudad 2',
            province='Provincia 2',
            owner=self.user
        )

    def test_client_list_view(self):
        """
        Verificamos que la vista de lista de clientes devuelve la respuesta correcta
        y muestra los clientes asociados al usuario autenticado.
        """
        # Hacer login con el usuario de prueba
        self.client.login(username='testuser', password='testpassword')

        # Hacer la petición GET a la URL de la lista de clientes
        response = self.client.get(reverse('list_clients'))

        # Verificamos que la respuesta es correcta
        self.assertEqual(response.status_code, 200)

        # Verificamos que los clientes asociados al usuario están en la respuesta
        self.assertContains(response, 'Cliente 1')
        self.assertContains(response, 'Cliente 2')

    def test_client_list_view_empty(self):
        """
        Verificamos que cuando el usuario no tiene clientes, la vista de lista
        de clientes muestra un mensaje adecuado.
        """
        # Crear un usuario sin clientes
        self.user_without_clients = User.objects.create_user(username='emptyuser', password='emptyuserpass')

        # Hacer login con el nuevo usuario sin clientes
        self.client.login(username='emptyuser', password='emptyuserpass')

        # Hacer la petición GET a la URL de la lista de clientes
        response = self.client.get(reverse('list_clients'))

        # Verificamos que la respuesta es correcta
        self.assertEqual(response.status_code, 200)

        # Verificamos que el mensaje de no hay resultados se muestra cuando no hay clientes
        self.assertContains(response, 'No se ha encontrado ningún cliente')

    def test_client_upsert_view_create(self):
        """
        Verificamos que la vista de creación de cliente funciona correctamente
        y que el cliente es creado en la base de datos.
        """
        # Hacer login con el usuario de prueba
        self.client.login(username='testuser', password='testpassword')

        # Definir los datos para la creación de un nuevo cliente
        client_data = {
            'name': 'Nuevo Cliente',
            'nif': 'W7995303J',
            'address': 'Calle 3, 345',
            'city': 'Ciudad 3',
            'province': 'Provincia 3',
        }

        # Hacer la petición POST para crear un cliente
        response = self.client.post(reverse('add_client'), client_data)

        # Verificamos que la respuesta es correcta (redirección a la lista de clientes)
        self.assertRedirects(response, reverse('list_clients'))

        # Verificamos que el cliente se ha creado en la base de datos
        self.assertTrue(Client.objects.filter(nif='W7995303J').exists())

    def test_client_upsert_view_edit(self):
        """
        Verificamos que la vista de edición de cliente funciona correctamente
        y que los cambios se guardan en la base de datos.
        """
        # Hacer login con el usuario de prueba
        self.client.login(username='testuser', password='testpassword')

        # Definir los datos para editar un cliente existente
        updated_data = {
            'name': 'Cliente Editado',
            'nif': '78687592S',  # Mantener el mismo NIF
            'address': 'Calle 1, 123 (editada)',
            'city': 'Ciudad 1',
            'province': 'Provincia 1',
        }

        # Hacer la petición POST para editar el cliente
        response = self.client.post(reverse('edit_client', kwargs={'pk': self.client1.pk}), updated_data)

        # Verificamos que la respuesta es correcta (redirección a la lista de clientes)
        self.assertRedirects(response, reverse('list_clients'))

        # Verificamos que los datos del cliente se han actualizado en la base de datos
        self.client1.refresh_from_db()  # Recargar el cliente desde la base de datos
        self.assertEqual(self.client1.address, 'Calle 1, 123 (editada)')

    def test_client_list_view_other_user_clients(self):
        """
        Verificamos que un usuario autenticado no puede ver los clientes de otro usuario.
        """
        # Crear un segundo usuario de prueba
        other_user = User.objects.create_user(username='otheruser', password='otherpassword')

        # Crear clientes asociados al segundo usuario
        client3 = Client.objects.create(
            name='Cliente 3',
            nif='34567890C',
            address='Calle 3, 345',
            city='Ciudad 3',
            province='Provincia 3',
            owner=other_user
        )

        # Hacer login con el primer usuario (no el que tiene cliente3)
        self.client.login(username='testuser', password='testpassword')

        # Hacer la petición GET a la URL de la lista de clientes
        response = self.client.get(reverse('list_clients'))

        # Verificamos que la respuesta es correcta
        self.assertEqual(response.status_code, 200)

        # Verificamos que el cliente del otro usuario no está en la respuesta
        self.assertNotContains(response, 'Cliente 3')

    # def test_anonymous_user_access_list(self):
    #     # Test para verificar que un usuario anónimo no pueda acceder al listado
    #     response = self.client.get(self.list_url)
    #     self.assertRedirects(response, f'/accounts/login/?next={self.list_url}')
    #
    # def test_anonymous_user_access_create(self):
    #     # Test para verificar que un usuario anónimo no pueda acceder a la creación de cliente
    #     response = self.client.get(self.create_url)
    #     self.assertRedirects(response, f'/accounts/login/?next={self.create_url}')
    #
    # def test_anonymous_user_access_edit(self):
    #     # Test para verificar que un usuario anónimo no pueda acceder a la edición de cliente
    #     response = self.client.get(self.edit_url)
    #     self.assertRedirects(response, f'/accounts/login/?next={self.edit_url}')
