# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import (
    Imovel,
    Anuncio,
    Reserva
)

from .validators import (
    DataCheckInValidator,
    ReservaDisponivelValidator,
    AcomodacoesDisponiveisValidator
)


class ImovelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Imovel
        fields = '__all__'


class AnuncioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Anuncio
        fields = '__all__'


class ReservaSerializer(serializers.ModelSerializer):
    codigo = serializers.CharField(read_only=True)

    class Meta:
        model = Reserva
        fields = '__all__'
        validators = [
            DataCheckInValidator(),
            AcomodacoesDisponiveisValidator(),
            ReservaDisponivelValidator()]
