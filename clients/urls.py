from django.urls import path

from . import views

urlpatterns = [
    path("", views.list_clients, name="list_clients"),
    # path("new/", views.agregar_client, name="add_client"),
    path("new/", views.ClientUpsertView.as_view(), name="add_client"),
    path('edit/<int:pk>/', views.ClientUpsertView.as_view(), name='edit_client'),

]
