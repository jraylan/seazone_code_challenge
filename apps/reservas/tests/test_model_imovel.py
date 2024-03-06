from django.test import TestCase
from django.db.transaction import TransactionManagementError
from django.db.utils import IntegrityError


from apps.reservas.models import Imovel


CREATE_IMOVEL_DATA = {
    "codigo": "Casa Teste 101",
    "capacidade": 3,
    "banheiros": 1,
    "aceita_animais": True,
    "taxa_limpeza": 150.00,
    "data_ativacao": "2024-03-05"
}



class ImovelModelTestCase(TestCase):
    fixtures = ["test_db_backup.json"]


    def test_model_creation(self):
        try:
            Imovel.objects.create(
                **CREATE_IMOVEL_DATA
            )
        except Exception:
            self.fail("Não foi possível criar uma instância do modelo Imóvel")


    def test_model_validations(self):
        """Testa as constraints na criação do modelo"""
        with self.assertRaises(
                (IntegrityError, TransactionManagementError),
                msg="A validação constraint no campo 'capacidade' não foi acionada."):
            Imovel.objects.create(**{
                **CREATE_IMOVEL_DATA,
                "capacidade": 0})
            
        with self.assertRaises(
                (IntegrityError, TransactionManagementError),
                msg="A validação constraint no campo 'banheiros' não foi acionada."):
            Imovel.objects.create(**{
                **CREATE_IMOVEL_DATA,
                "banheiros": -1})
    
        with self.assertRaises(
                (IntegrityError, TransactionManagementError),
                msg="A validação constraint no campo 'taxa_limpeza' não foi acionada."):
            Imovel.objects.create(**{
                **CREATE_IMOVEL_DATA,
                "taxa_limpeza": -1.0})