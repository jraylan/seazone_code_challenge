from apps.reservas.serializers import ImovelSerializer
from .base import *


READ_IMOVEL_PK = 1
UPDATE_IMOVEL_PK = 2
DELETE_IMOVEL_PK = 3


CREATE_IMOVEL_DATA = {
    "codigo": "Casa Teste 10",
    "capacidade": 4,
    "banheiros": 2,
    "aceita_animais": False,
    "taxa_limpeza": "10.00",
    "data_ativacao": "2024-01-06"
}

TESTE_IMOVEL_DATA = {
    "codigo": "Casa Teste 2",
    "capacidade": 5,
    "banheiros": 3,
    "aceita_animais": True,
    "taxa_limpeza": "50.00",
    "data_ativacao": "2024-01-08"
}

UPDATE_IMOVEL_DATA = {
    "codigo": "Casa Teste 11",
    "capacidade": 5,
    "banheiros": 3,
    "aceita_animais": True,
    "taxa_limpeza": "50.00",
    "data_ativacao": "2024-01-08"
}


class ImovelApiTestCase(BaseApiTestCase):
    url_name = "imovel_api_view"
    serializer_class = ImovelSerializer

    def test_list_imovel(self):
        response = self.check_api_view_list()
        response_json = response.json()
        self.assertGreater(len(response_json), 0,
                           "A listagem não retornou nenhum objeto")

        for obj in response_json:
            self.check_serialization(obj)


    def test_create_imovel(self):
        # Verifica se os dados de testes não apresentam erros de validação
        self.assertNoValidationErrors(
            CREATE_IMOVEL_DATA, "Houve um erro na validação dos dados de teste de criação de imóvel.")

        # Verifica a chamada da api de criação
        response = self.check_api_view_create(CREATE_IMOVEL_DATA)

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
        self.assertValidationError({}, 'codigo', 'required')
        self.assertValidationError({}, 'capacidade', 'required')
        self.assertValidationError({}, 'banheiros', 'required')
        self.assertValidationError({"capacidade": 0}, 'capacidade', 'min_value')
        self.assertValidationError({"banheiros": -1}, 'banheiros', 'min_value')
        self.assertValidationError(TESTE_IMOVEL_DATA, 'codigo', 'unique')

        # Verifica validação na criação de imóvel
        self.check_api_view_create({}, 400)

    def test_read_imovel(self):
        # Certifica-se de que o objeto está no banco antes de iniciar o teste.
        self.assertObjectPresent(
            READ_IMOVEL_PK,
            f"O imóvel com id '{READ_IMOVEL_PK}' não foi encontrado no banco de dados."
            "O teste não poderá ser realizado")

        self.check_api_view_read(READ_IMOVEL_PK)

    def test_update_imovel(self):
        # Certifica-se de que o objeto está no banco antes de iniciar o teste.
        self.assertObjectPresent(
            UPDATE_IMOVEL_PK,
            f"O imóvel com id '{UPDATE_IMOVEL_PK}' não foi encontrado no banco de dados. "
            "O teste não poderá ser realizado")

        # Verifica a chamada da API
        response = self.check_api_view_update(
            UPDATE_IMOVEL_PK, UPDATE_IMOVEL_DATA, expected_status_code=200)

        try:
            response_json = response.json()
        except JSONDecodeError:
            self.fail("A requisição não retornou um JSON válido.")

        for k, v in UPDATE_IMOVEL_DATA.items():
            if k not in response_json:
                self.fail(
                    f'O campo alterado "{k}" não está presente nos dados da resposta.')

            # Checar apenas dados primitivos
            if isinstance(v, (int, str, bool, float)):
                if response_json[k] != v:
                    self.fail(
                        f'O valor do campo "{k}" não foi atualizado. '
                        f'Esperado: "{v}". Encontrado: "{response_json[k]}"')

    def test_delete_imovel(self):
        # Certifica-se de que o objeto está no banco antes de iniciar o teste.
        self.assertObjectPresent(
            DELETE_IMOVEL_PK,
            f"O imóvel com id '{DELETE_IMOVEL_PK}' não foi encontrado no banco de dados."
            "O teste não poderá ser realizado")

        # Verifica o chamado da API
        self.check_api_view_delete(DELETE_IMOVEL_PK, expected_status_code=204)

        # Certifica-se que o objeto foi excluído
        self.assertObjectNotPresent(
            DELETE_IMOVEL_PK,
            f"O imóvel com id '{DELETE_IMOVEL_PK}' foi encontrado no banco de dados.")
