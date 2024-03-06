from django.test import TestCase
from django.db.transaction import TransactionManagementError
from django.db.utils import IntegrityError


from apps.reservas.models import Anuncio, Imovel



CREATE_ANUNCIO_DATA = {
    "imovel_id": 1,
    "plataforma": "AirBnB",
    "taxa_plataforma": 1.00
}


class AnuncioModelTestCase(TestCase):
    fixtures = ["test_db_backup.json"]


    def test_model_creation(self):
        try:
            Anuncio.objects.create(**CREATE_ANUNCIO_DATA)
        except Exception:
            self.fail("Não foi possível criar uma instância do objeto Imóvel")

    def test_model_validations(self):
        """Testa as constraints na criação do modelo"""

        with self.assertRaises(
            (IntegrityError, TransactionManagementError),
            msg="A validação da chave estrangeira não foi acionada."):
            Anuncio.objects.create(**{
                **CREATE_ANUNCIO_DATA,
                "imovel_id": None})
