# -*- coding: utf-8 -*-

from django.urls import re_path
from . import views

urlpatterns = [
    #
    re_path(r'imoveis/?$',
        views.ImovelAPIView.as_view(), name="imovel_api_view"),
    re_path(r'imoveis/(?P<pk>[0-9]+)/?$',
        views.ImovelAPIView.as_view(), name="imovel_api_view"),
    #
    re_path(r'anuncios/?$',
        views.AnuncioAPIView.as_view(), name="anuncio_api_view"),
    re_path(r'anuncios/(?P<pk>[0-9]+)/?$',
        views.AnuncioAPIView.as_view(), name="anuncio_api_view"),
    #
    re_path(r'reservas/?$',
        views.ReservaAPIView.as_view(), name="reserva_api_view"),
    re_path(r'reservas/(?P<pk>[0-9]+)/?$',
        views.ReservaAPIView.as_view(), name="reserva_api_view"),
]