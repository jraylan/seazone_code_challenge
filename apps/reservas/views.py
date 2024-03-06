# -*- coding: utf-8 -*-
from rest_framework import mixins
from rest_framework import generics

from .models import (
    Imovel,
    Anuncio,
    Reserva
)

from .serializers import (
    ImovelSerializer,
    AnuncioSerializer,
    ReservaSerializer
)


class BaseModelAPIView(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        generics.GenericAPIView):
    """Classe que serve de base para as outras views. Esta classe implementa
    as features compartilhadas pelas outras views, são elas: listagem; criação
    e recuperação de objetos. A classe também herda os mixins para ajudar na
    realização de atualização e remoção, no entanto os métodos put e delete
    precisam ser implementados nas classes herdeiras."""
    model = None

    # Quando True, enviar o post na url com o id do objeto irá atualizar-lo
    # o método put precisa ser implementado
    atualizar_via_post = False    
    lookup_url_kwarg = 'pk'
        
    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, pk=None, format=None):
        if pk:
            return self.retrieve(request, format=format)
        return self.list(request, format=format)
    
    def post(self, request, pk=None, format=None):
        if pk:
            # Permitir alteração criação via post?
            if self.atualizar_via_post and hasattr(self, 'put'):
                # Se permitido, tratar como um PUT
                return self.put(request, format=format)            
            # Retornar 405 já que o POST na url sem o pk não é um método válido
            return self.http_method_not_allowed(request)

        return self.create(request, format=format)


class ImovelAPIView(BaseModelAPIView):    
    model = Imovel
    serializer_class = ImovelSerializer

    def put(self, request, pk=None, format=None):
        return self.update(request, pk=pk, format=format)

    def delete(self, request, pk=None, format=None):
        return self.destroy(request, pk=pk, format=format)


class AnuncioAPIView(BaseModelAPIView):
    model = Anuncio
    serializer_class = AnuncioSerializer

    def put(self, request, pk=None, format=None):
        return self.update(request, pk=pk, format=format)


class ReservaAPIView(BaseModelAPIView):
    model = Reserva
    serializer_class = ReservaSerializer

    def delete(self, request, pk=None, format=None):
        return self.destroy(request, pk=pk, format=format)

