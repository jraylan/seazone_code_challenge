# -*- coding: utf-8 -*-
from django.utils.translation import gettext as _


VALIDADOR_CAPACIDADE = _('O imóvel deve comportar ao menos um hóspede.')

VALIDADOR_TAXA_LIMPEZA = _('A taxa de limpeza não pode possuir um valor negativo.')

VALIDADOR_TAXA_PLATAFORMA =_(
    'A taxa da plataforma não pode possuir um valor negativo.')

VALIDADOR_PRECO_TOTAL = _('O preço total não pode possuir um valor negativo.')

VALIDADOR_HOSPEDES = _('A reserva deve possuir ao menos um hóspede.')

VALIDADOR_CHECKIN_DATA = _('A data de check-in não pode ser posterior à data de check-out.')

VALIDADOR_RESERVA_INDISPONIVEL = _(
    'Imóvel não disponível em um ou mais dias do intervalo selecionado.')

VALIDADOR_ACOMODACOES = _(
    'O imóvel não pode acomodar todos os hospedes. '
    'O limite de hospedes no imóvel é %(capacidade)s, %(excedente)s a mais que a quantidade indicada')
