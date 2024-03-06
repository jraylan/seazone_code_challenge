from django.test import TestCase
from django.db.transaction import TransactionManagementError
from django.db.utils import IntegrityError


from apps.reservas.models import Reserva


CREATE_RESERVA_DATA = {
    "data_checkin": "2024-12-08",
    "data_checkout": "2024-12-09",
    "preco_total": "100.00",
    "comentario": "Lorem ipsum dolor sit amet, consectetur adip.",
    "qtd_hospedes": 2,
    "anuncio_id": 5
}



class ReservaModelTestCase(TestCase):
    fixtures = ["test_db_backup.json"]


    def test_model_creation(self):
        try:
            Reserva.objects.create(
                **CREATE_RESERVA_DATA
            )
        except Exception:
            self.fail("Não foi possível criar uma instância do modelo Reserva")


    def test_model_validations(self):
        """Testa as constraints na criação do modelo"""
        with self.assertRaises(
                (IntegrityError, TransactionManagementError),
                msg="A validação constraint no campo 'preco_total' não foi acionada."):
            Reserva.objects.create(**{
                **CREATE_RESERVA_DATA,
                "preco_total": 0})
            
        with self.assertRaises(
                (IntegrityError, TransactionManagementError),
                msg="A validação constraint no campo 'qtd_hospedes' não foi acionada."):
            Reserva.objects.create(**{
                **CREATE_RESERVA_DATA,
                "qtd_hospedes": 0})