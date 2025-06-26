import unittest
from app_teste import app  # importa sua app Flask
from unittest.mock import patch



class PrevisaoTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    @patch("app.loaded_models")
    @patch("app.scaler")
    @patch("app.explainer")
    def test_previsao_endpoint(self, mock_explainer, mock_scaler, mock_loaded_models):

        mock_loaded_models.keys.return_value = ['xgboost', 'dt', 'lr', 'nb', 'rf', 'svm']

        # Configura mocks
        mock_model = unittest.mock.Mock()
        mock_model.predict.return_value = [1]
        mock_model.predict_proba.return_value = [[0.1, 0.9]]
        mock_loaded_models.__getitem__.side_effect = lambda k: mock_model
        mock_scaler.transform.return_value = [[0.5, 0.5]]

        # Simular explainer LIME
        mock_exp = unittest.mock.Mock()
        mock_exp.as_pyplot_figure.return_value = unittest.mock.Mock()
        mock_explainer.explain_instance.return_value = mock_exp

        # Dados simulados para o formulário
        form_data = {
            "tenure": "12",
            "monthlyCharges": "70.5",
            "internetService": "dsl",
            "contract": "monthly",
            "paymentMethod": "credit_card",
            "dependents": "yes",
            "onlineSecurity": "yes",
            "techSupport": "yes",
            "paperlessBilling": "yes",
            "modeloEscolhido": "xgboost"
        }

        response = self.client.post("/previsao", data=form_data)

        # Verificações básicas
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Churn", response.data)  # depende do valor retornado
        self.assertIn(b"Probabilidade", response.data)



    def test_previsao_invalid_value(self):
        form_data = {
            "tenure": "abc",  # inválido
            "monthlyCharges": "-10",  # inválido
            "internetService": "dsl",
            "contract": "monthly",
            "paymentMethod": "credit_card",
            "dependents": "yes",
            "onlineSecurity": "yes",
            "techSupport": "yes",
            "paperlessBilling": "yes",
            "modeloEscolhido": "xgboost"
        }
        response = self.client.post("/previsao", data=form_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Valores inválidos", response.data.decode("utf-8"))


    def test_previsao_missing_field(self):
        form_data = {
            "monthlyCharges": "70.5",
            "internetService": "dsl",
            # falta 'tenure'
            "contract": "monthly",
            "paymentMethod": "credit_card",
            "dependents": "yes",
            "onlineSecurity": "yes",
            "techSupport": "yes",
            "paperlessBilling": "yes",
            "modeloEscolhido": "xgboost"
        }
        response = self.client.post("/previsao", data=form_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Campo 'tenure'", response.data)


    def test_previsao_unknown_model(self):
        form_data = {
            "tenure": "12",
            "monthlyCharges": "70.5",
            "internetService": "dsl",
            "contract": "monthly",
            "paymentMethod": "credit_card",
            "dependents": "yes",
            "onlineSecurity": "yes",
            "techSupport": "yes",
            "paperlessBilling": "yes",
            "modeloEscolhido": "modelo_inexistente"
        }
        response = self.client.post("/previsao", data=form_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Modelo desconhecido", response.data)

if __name__ == "__main__":
    unittest.main()