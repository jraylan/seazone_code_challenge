# -*- coding: utf-8 -*-
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q, F
from django.utils.translation import gettext as _

from uuid import uuid4

# Módulo para concentrar mensagens e afins, para manter o código limpo
from .constants import (
    VALIDADOR_CAPACIDADE,
    VALIDADOR_TAXA_LIMPEZA,
    VALIDADOR_TAXA_PLATAFORMA,
    VALIDADOR_PRECO_TOTAL,
    VALIDADOR_HOSPEDES
)


class ModeloAuditavel(models.Model):
    """Modelo abstrato que adiciona campos para armazenar de forma automática
    a data e hora da criação e atualização nos modelos que herdam desta classe"""
    data_cadastro = models.DateTimeField(
        _("Data de Cadastro"), auto_now_add=True)
    data_atualizacao = models.DateTimeField(
        _("Data de Atualização"), auto_now=True)
    
    class Meta:
        abstract = True


class Imovel(ModeloAuditavel):
    """Modelo que armazena as informações dos imóveis"""
    # O tipo de valor do código do imóvel não foi especificado, sendo assim
    # estou assumindo que o código deve ser a descrição do imóvel, tendo em
    # vista que esta informação me parece ser pertinente.
    codigo = models.CharField(
        _('Código'), max_length=255, null=False, blank=False, unique=True)
    capacidade = models.PositiveSmallIntegerField(
        _("Capacidade de Hospedagem"), blank=False, null=False, validators=[
            MinValueValidator(limit_value=1, message=VALIDADOR_CAPACIDADE)])
    banheiros = models.PositiveSmallIntegerField(
        _("Banheiros"), blank=False, null=False)
    aceita_animais = models.BooleanField(
        _("Aceita Animais"), default=False, blank=True)
    taxa_limpeza = models.DecimalField(
        _("Taxa de Limpeza"), max_digits=5, decimal_places=2, default=Decimal('0.00'),
        validators=[MinValueValidator(limit_value=0, message=VALIDADOR_TAXA_LIMPEZA)])
    data_ativacao = models.DateField(
        _("Data de Ativação"), default=None, null=True, db_index=True)


    class Meta:
        verbose_name = _("Imóvel")
        verbose_name_plural = _("Imóveis")
        constraints = (
            models.CheckConstraint(
                check=Q(capacidade__gte=1), name="capacidade_min_val"),
            models.CheckConstraint(
                check=Q(banheiros__gte=0), name="banheiros_min_val"),
            models.CheckConstraint(
                check=Q(taxa_limpeza__gte=0.0), name="taxa_limpeza_min_val"))

    def __str__(self):
        return f'{self._meta.verbose_name}: {self.codigo}'


class Anuncio(ModeloAuditavel):
    """Modelo que armazena as informações de anúncios"""
    imovel = models.ForeignKey(Imovel, verbose_name=_(
        "Imóvel"), on_delete=models.CASCADE, related_name="anuncios")
    plataforma = models.CharField(
        _("Plataforma"), max_length=50, null=False, blank=False)
    taxa_plataforma = models.DecimalField(
        _("Taxa da Plataforma"), max_digits=5, decimal_places=2, default=Decimal('0.00'),
        validators=[MinValueValidator(limit_value=0, message=VALIDADOR_TAXA_PLATAFORMA)])
    
    class Meta:
        verbose_name = _("Anúncio")
        verbose_name_plural = _("Anúncios")

    def __str__(self):
        return f'{self._meta.verbose_name}: {self.plataforma} - {self.imovel_id}'


class Reserva(ModeloAuditavel):
    """Modelo que armazena as informações de reservas"""
    anuncio = models.ForeignKey(Anuncio, verbose_name=_(
        "Anúncio"), on_delete=models.CASCADE, related_name="reservas")
    #  O tipo de valor do código da reserva não foi especificado então algumas
    # opções foram consideradas, duas delas foram as seguintes:
    #
    # * Utilizar um campo positive small integer ou char field e gerar os
    # valores de forma aleatória;
    # * Utilizar um campo UUID com um valor default definido com a função uuid4
    #
    #  A opção escolhida foi a segunda pela praticidade, tendo em vista que ao
    # gerar valores aleatórios existe a possibilidade de ocorrer choques com
    # valores já existentes, o que causaria um erro devido a unique constraint
    # exigida por este campo. Outra possibilidade seria utilizar o hash gerado
    # a partir de alguma informação, mas por hora, esta foi a solução escolhida .
    # 
    #  Esta decisão foi tomada sem levar em consideração a experiência de
    # usuário. Códigos UUID são difíceis de memorizar e são relativamente 
    # grande, o que os tornam uma opção menos amagáveis para usuários finais.
    # Isto não foi considerado pôs não está no escopo do desafio como este
    # campo será apresentado para o usuário final.
    codigo = models.UUIDField(
        _("Código da reserva"), default=uuid4, null=False, blank=False, unique=True)
    data_checkin = models.DateField(
        _("Check-in"), null=False, blank=False, db_index=True)
    data_checkout = models.DateField(
        _("Check-out"), null=False, blank=False, db_index=True)
    preco_total = models.DecimalField(
        _("Preço Total"), max_digits=5, decimal_places=2, validators=[
            MinValueValidator(limit_value=0.01, message=VALIDADOR_PRECO_TOTAL)])
    # Como a quantidade de caracteres do campo de comentários não foi especificado
    # será utilizado um campo do tipo text
    comentario = models.TextField(_("Comentário"), null=True)
    qtd_hospedes = models.PositiveSmallIntegerField(
        _("Número de Hospedes"), null=False, blank=False, validators=[
            MinValueValidator(limit_value=1, message=VALIDADOR_HOSPEDES)])

    class Meta:
        verbose_name = _("Reserva")
        verbose_name_plural = _("Reservas")
        constraints = (
            models.CheckConstraint(
                check=Q(data_checkin__lte=F('data_checkout')), name="checkin_lte_checkout"),
            models.CheckConstraint(
                check=Q(qtd_hospedes__gte=1), name="qtd_hospedes_min_val"),
            models.CheckConstraint(
                check=Q(preco_total__gte=0.01), name="preco_total_min_val")
        )

    def __str__(self):
        return f'{self._meta.verbose_name}: {self.codigo}'

