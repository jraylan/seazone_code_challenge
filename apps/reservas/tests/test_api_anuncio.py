from apps.reservas.serializers import AnuncioSerializer
from .base import *


READ_ANUNCIO_PK = 1
UPDATE_ANUNCIO_PK = 2
DELETE_ANUNCIO_PK = 3


CREATE_ANUNCIO_DATA = {
    "plataforma": "AirBnb",
    "taxa_plataforma": "10.00",
    "imovel": 1
}

UPDATE_ANUNCIO_DATA = {
    "plataforma": "booking.com",
    "imovel": 1
}



class AnuncioApiTestCase(BaseApiTestCase):
    url_name = "anuncio_api_view"
    serializer_class = AnuncioSerializer
    

    def test_list_anuncio(self):
        response = self.check_api_view_list()
        response_json = response.json()
        self.assertGreater(len(response_json), 0,
                           "A listagem não retornou nenhum objeto")
        
        # Valida todos os itens retornados
        for obj in response_json:
            self.check_serialization(obj)


    def test_create_anuncio(self):
        # Verifica se os dados de testes não apresentam erros de validação
        self.assertNoValidationErrors(
            CREATE_ANUNCIO_DATA, "Houve um erro na validação dos dados de teste de criação de anúncio.")
        
        # Verifica a chamada da api de criação
        response = self.check_api_view_create(CREATE_ANUNCIO_DATA)

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
        self.assertValidationError({}, 'plataforma', 'required')
        self.assertValidationError({}, 'imovel', 'required')
        self.assertValidationError(
            {'taxa_plataforma': -2.00}, 'taxa_plataforma', 'min_value')

        # Verifica validação na criação de anúncio
        self.check_api_view_create({}, 400)
        

    def test_read_anuncio(self):
        # Certifica-se de que o objeto está no banco antes de iniciar o teste.
        self.assertObjectPresent(
            READ_ANUNCIO_PK,
            f"O anúncio com id '{READ_ANUNCIO_PK}' não foi encontrado no banco de dados."
            "O teste não poderá ser realizado")
        
        self.check_api_view_read(READ_ANUNCIO_PK)
    

    def test_update_anuncio(self):
        # Certifica-se de que o objeto está no banco antes de iniciar o teste.
        self.assertObjectPresent(
            UPDATE_ANUNCIO_PK,
            f"O anúncio com id '{UPDATE_ANUNCIO_PK}' não foi encontrado no banco de dados. "
            "O teste não poderá ser realizado")
        
        # Verifica a chamada da API
        response = self.check_api_view_update(
            UPDATE_ANUNCIO_PK, UPDATE_ANUNCIO_DATA, expected_status_code=200)

        try:
            response_json = response.json()
        except JSONDecodeError:
            self.fail("A requisição não retornou um JSON válido.")

        for k, v in UPDATE_ANUNCIO_DATA.items():
            if k not in response_json:
                self.fail(
                    f'O campo alterado "{k}" não está presente nos dados da resposta.')
                
            # Checar apenas dados primitivos
            if isinstance(v, (int, str, bool, float)):
                if response_json[k] != v:
                    self.fail(
                        f'O valor do campo "{k}" não foi atualizado. '
                        f'Esperado: "{v}". Encontrado: "{response_json[k]}"')


    def test_delete_anuncio(self):
        # Certifica-se de que o objeto está no banco antes de iniciar o teste.
        self.assertObjectPresent(
            DELETE_ANUNCIO_PK,
            f"O anúncio com id '{DELETE_ANUNCIO_PK}' não foi encontrado no banco de dados."
            "O teste não poderá ser realizado")
        
        # Verifica o chamado da API
        self.check_api_view_delete(DELETE_ANUNCIO_PK, expected_status_code=405)

        # Certifica-se que o objeto não foi excluído
        self.assertObjectPresent(
            DELETE_ANUNCIO_PK,
            f"O anúncio com id '{DELETE_ANUNCIO_PK}' não foi encontrado no banco de dados.")

