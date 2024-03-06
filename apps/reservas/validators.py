# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.db.models import Q, F

from .constants import (
    VALIDADOR_CHECKIN_DATA,
    VALIDADOR_RESERVA_INDISPONIVEL,
    VALIDADOR_ACOMODACOES
)


from .models import Reserva


class DataCheckInValidator:
    """Valida se a data do check-in é maior que a data do check-out"""

    def __call__(self, values):
        data_checkin = values['data_checkin']
        data_checkout = values['data_checkout']

        if data_checkin > data_checkout:
            raise serializers.ValidationError({
                'data_checkin': VALIDADOR_CHECKIN_DATA
            })


class ReservaDisponivelValidator:
    """Valida se o imóvel está disponível para reserva no período

    Args:
        **data_checkout_disponivel (bool): Indica se o imóvel está
        disponível na data do checkout de uma reserva.
    """

    data_checkout_disponivel = False
    requires_context = True

    def __init__(self, data_checkout_disponivel: bool=False):
        self.data_checkout_disponivel = data_checkout_disponivel

    def __call__(self, values, serializer_field):
        anuncio = values['anuncio']
        data_checkin = values['data_checkin']
        data_checkout = values['data_checkout']

        query = Q(anuncio__imovel=anuncio.imovel_id)
        
        # Verifica se trata-se de uma instância existente.
        # Caso seja, é necessário remover esta instância da
        # checagem
        if values.get('id'):
            query.add(~Q(id=values['id']), Q.AND)
        elif getattr(serializer_field, 'instance', None):
            query.add(
                ~Q(id=serializer_field.instance.id), Q.AND)

        if self.data_checkout_disponivel:
            query.add(
                Q(data_checkout__gt=data_checkin,
                  data_checkin__lt=data_checkout), Q.AND)
        else:
            query.add(
                Q(data_checkout__gte=data_checkin,
                  data_checkin__lte=data_checkout), Q.AND)

        if Reserva.objects.filter(query).exists():
            raise serializers.ValidationError(VALIDADOR_RESERVA_INDISPONIVEL, "conflict")


class AcomodacoesDisponiveisValidator:
    """Valida se o imóvel acomoda a quantidade de hospedes"""

    def __call__(self, values):
        anuncio = values['anuncio']
        qtd_hospedes = values['qtd_hospedes']
        capacidade = anuncio.imovel.capacidade

        if capacidade < qtd_hospedes:
            raise serializers.ValidationError({
                'qtd_hospedes': VALIDADOR_ACOMODACOES % {
                    'capacidade': capacidade,
                    'excedente': qtd_hospedes - capacidade
                }
            })

