
import unittest
from app_teste import app
import io
import pandas as pd

class PrevisaoCsvTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_previsao_csv_success(self):
        # Criar um CSV em memória com colunas compatíveis com o preprocess_data()
        csv_data = (
            "tenure,MonthlyCharges,InternetService_DSL,InternetService_Fiber optic,InternetService_No,Contract_Month-to-month,Contract_One year,Contract_Two year,PaymentMethod_Bank transfer (automatic),PaymentMethod_Credit card (automatic),PaymentMethod_Electronic check,PaymentMethod_Mailed check,Dependents_Yes,OnlineSecurity_Yes,TechSupport_Yes,PaperlessBilling_Yes\n"
            "1,170.35,0,1,0,1,0,0,0,0,1,0,0,0,0,1\n"
        )

        data = {
            'modeloEscolhido': 'rf',  # modelo existente no teu loaded_models
            'csvfile': (io.BytesIO(csv_data.encode('utf-8')), 'test.csv')
        }

        response = self.app.post('/previsao-csv', data=data, content_type='multipart/form-data', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        html_content = response.data.decode('utf-8')
        self.assertIn('Previsão feita, o resultado será descarregado automaticamente.', html_content)

    def test_previsao_csv_missing_file(self):
        # Enviar sem ficheiro
        data = {
            'modeloEscolhido': 'rf'
        }

        response = self.app.post('/previsao-csv', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Ficheiro CSV não enviado", response.data.decode('utf-8'))

    def test_previsao_csv_empty_file(self):
        # Enviar CSV vazio
        data = {
            'modeloEscolhido': 'rf',
            'csvfile': (io.BytesIO(b''), 'empty.csv')
        }

        response = self.app.post('/previsao-csv', data=data, content_type='multipart/form-data')
        # Como pandas falha ao ler CSV vazio, retorna 500
        self.assertEqual(response.status_code, 500)
        self.assertIn("Erro ao processar o ficheiro CSV", response.data.decode('utf-8'))

    def test_previsao_csv_model_not_found(self):
        # Tentar usar modelo inexistente
        csv_data = (
            "dependents,tenure,internetService,onlineSecurity,techSupport,contract,paperlessBilling,paymentMethod,monthlyCharges\n"
            "1,12,Fiber optic,Yes,No,Month-to-month,Yes,Credit card (automatic),89.5\n"
        )

        data = {
            'modeloEscolhido': 'modelo_inexistente',
            'csvfile': (io.BytesIO(csv_data.encode('utf-8')), 'test.csv')
        }

        response = self.app.post('/previsao-csv', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
