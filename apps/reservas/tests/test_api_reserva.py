from apps.reservas.serializers import ReservaSerializer
from .base import *


READ_RESERVA_PK = 1
UPDATE_RESERVA_PK = 2
DELETE_RESERVA_PK = 3


CREATE_RESERVA_DATA = {
    "data_checkin": "2024-05-08",
    "data_checkout": "2024-05-09",
    "preco_total": "100.00",
    "comentario": None,
    "qtd_hospedes": 2,
    "anuncio": 5
}

TESTE_RESERVA_DATA = {
    "data_checkin": "2024-03-04",
    "data_checkout": "2024-03-09",
    "preco_total": "100.00",
    "comentario": None,
    "qtd_hospedes": 2,
    "anuncio": 5
}


class ReservaApiTestCase(BaseApiTestCase):
    url_name = "reserva_api_view"
    serializer_class = ReservaSerializer

    def test_list_reserva(self):
        response = self.check_api_view_list()
        response_json = response.json()
        self.assertGreater(len(response_json), 0,
                           "A listagem não retornou nenhum objeto")
        
        # Valida todos os itens retornados
        for obj in response_json:
            self.check_serialization(obj)


    def test_create_reserva(self):
        # Verifica se os dados de testes não apresentam erros de validação
        self.assertNoValidationErrors(
            CREATE_RESERVA_DATA, "Houve um erro na validação dos dados de teste de criação de reserva.")

        # Verifica a chamada da api de criação
        response = self.check_api_view_create(CREATE_RESERVA_DATA)

        try:
            response_json = response.json()
        except JSONDecodeError:
            self.fail("A requisição não retornou um JSON válido.")

        pk = response_json.get('id')
        
        self.assertIsNotNone(
            pk, "Os dados da resposta da criação do objeto não retornou o id do mesmo.")

        # Verifica se o objeto foi criado
        self.assertObjectPresent(pk)

    def test_validations(self):
        # Verifica se os erros de validação estão sendo acionados
        self.assertValidationError({}, 'data_checkin', 'required')
        self.assertValidationError({}, 'data_checkout', 'required')
        self.assertValidationError({}, 'preco_total', 'required')
        self.assertValidationError({}, 'qtd_hospedes', 'required')
        self.assertValidationError({}, 'anuncio', 'required')
        self.assertValidationError({'preco_total': 0}, 'preco_total', 'min_value')
        self.assertValidationError({'qtd_hospedes': 0}, 'qtd_hospedes', 'min_value')
        self.assertValidationError(TESTE_RESERVA_DATA, 'non_field_errors', 'conflict')

        # Verifica validação na criação de reserva
        self.check_api_view_create({}, 400)

    def test_read_reserva(self):
        # Certifica-se de que o objeto está no banco antes de iniciar o teste.
        self.assertObjectPresent(
            READ_RESERVA_PK,
            f"O reserva com id '{READ_RESERVA_PK}' não foi encontrado no banco de dados."
            "O teste não poderá ser realizado")

        self.check_api_view_read(READ_RESERVA_PK)

    def test_update_reserva(self):
        # Certifica-se de que o objeto está no banco antes de iniciar o teste.
        self.assertObjectPresent(
            UPDATE_RESERVA_PK,
            f"O reserva com id '{UPDATE_RESERVA_PK}' não foi encontrado no banco de dados. "
            "O teste não poderá ser realizado")

        # Verifica a chamada da API
        response = self.check_api_view_update(
            UPDATE_RESERVA_PK, CREATE_RESERVA_DATA, expected_status_code=405)

        try:
            response.json()
        except JSONDecodeError:
            self.fail("A requisição não retornou um JSON válido.")

    def test_delete_reserva(self):
        # Certifica-se de que o objeto está no banco antes de iniciar o teste.
        self.assertObjectPresent(
            DELETE_RESERVA_PK,
            f"O reserva com id '{DELETE_RESERVA_PK}' não foi encontrado no banco de dados."
            "O teste não poderá ser realizado")

        # Verifica o chamado da API
        self.check_api_view_delete(DELETE_RESERVA_PK, expected_status_code=204)

        # Certifica-se que o objeto foi excluído
        self.assertObjectNotPresent(
            DELETE_RESERVA_PK,
            f"O reserva com id '{DELETE_RESERVA_PK}' foi encontrado no banco de dados.")
