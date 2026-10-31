"""
Testes de integração para a API do backend Flask do Calcify.
Verifica rotas, validações de parâmetros, tratamento de erros e respostas JSON.
"""

import json
import math
import unittest
from app import app


class TestCalcifyApp(unittest.TestCase):
    """Suíte de testes para a aplicação web Calcify."""

    def setUp(self):
        self.app = app
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def test_pagina_inicial(self):
        """Verifica se a página principal HTML é renderizada com sucesso."""
        resposta = self.client.get("/")
        self.assertEqual(resposta.status_code, 200)
        self.assertIn(b"Calcify", resposta.data)
        self.assertIn(b"Make numbers simple.", resposta.data)

    def test_status_api(self):
        """Verifica endpoint de health check."""
        resposta = self.client.get("/api/status")
        self.assertEqual(resposta.status_code, 200)
        dados = json.loads(resposta.data)
        self.assertEqual(dados["status"], "online")
        self.assertEqual(dados["aplicacao"], "Calcify")

    def test_calcular_operacoes_basicas(self):
        """Testa adição, subtração, multiplicação e divisão via API."""
        # Adição
        res = self.client.post("/api/calcular", json={"operacao": "adicionar", "a": 15, "b": 27})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)["resultado"], 42)

        # Subtração
        res = self.client.post("/api/calcular", json={"operacao": "subtrair", "a": 50, "b": 18})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)["resultado"], 32)

        # Multiplicação
        res = self.client.post("/api/calcular", json={"operacao": "multiplicar", "a": 6, "b": 7})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)["resultado"], 42)

        # Divisão
        res = self.client.post("/api/calcular", json={"operacao": "dividir", "a": 100, "b": 4})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)["resultado"], 25)

    def test_calcular_divisao_por_zero(self):
        """Verifica se a divisão por zero retorna erro amigável 400."""
        res = self.client.post("/api/calcular", json={"operacao": "dividir", "a": 10, "b": 0})
        self.assertEqual(res.status_code, 400)
        dados = json.loads(res.data)
        self.assertFalse(dados["success"])
        self.assertIn("Divisão por zero não é permitida", dados["error"])

    def test_calcular_porcentagem(self):
        """Testa endpoints de porcentagem."""
        res = self.client.post("/api/calcular", json={"operacao": "porcentagem_de_valor", "percentual": 20, "valor": 150})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)["resultado"], 30)

        res = self.client.post("/api/calcular", json={"operacao": "aumento_percentual", "valor": 100, "percentual": 15})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)["resultado"], 115)

        res = self.client.post("/api/calcular", json={"operacao": "desconto_percentual", "valor": 100, "percentual": 15})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)["resultado"], 85)

    def test_calcular_potencia_e_raizes(self):
        """Testa potência e raízes."""
        res = self.client.post("/api/calcular", json={"operacao": "potencia", "base": 2, "expoente": 3})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)["resultado"], 8)

        res = self.client.post("/api/calcular", json={"operacao": "raiz_quadrada", "radicando": 64})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)["resultado"], 8)

        res = self.client.post("/api/calcular", json={"operacao": "raiz_enesima", "radicando": 27, "indice": 3})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)["resultado"], 3)

    def test_calcular_trigonometria_e_cientifica(self):
        """Testa funções científicas."""
        res = self.client.post("/api/calcular", json={"operacao": "seno", "angulo": 90, "em_graus": True})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)["resultado"], 1)

        res = self.client.post("/api/calcular", json={"operacao": "fatorial", "n": 5})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)["resultado"], 120)

        res = self.client.post("/api/calcular", json={"operacao": "logaritmo_base10", "x": 100})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)["resultado"], 2)

    def test_calcular_erros_invalidos(self):
        """Testa validações de erros matemáticos na API."""
        # Tangente de 90°
        res = self.client.post("/api/calcular", json={"operacao": "tangente", "angulo": 90, "em_graus": True})
        self.assertEqual(res.status_code, 400)
        self.assertIn("Tangente indefinida", json.loads(res.data)["error"])

        # Raiz quadrada de negativo
        res = self.client.post("/api/calcular", json={"operacao": "raiz_quadrada", "radicando": -4})
        self.assertEqual(res.status_code, 400)

        # Operação inexistente
        res = self.client.post("/api/calcular", json={"operacao": "inexistente"})
        self.assertEqual(res.status_code, 400)

    def test_api_equacoes(self):
        """Testa resolução de equações de 1º e 2º grau."""
        res = self.client.post("/api/equacao/primeiro-grau", json={"a": 3, "b": -9})
        self.assertEqual(res.status_code, 200)
        dados = json.loads(res.data)["dados"]
        self.assertEqual(dados["solucao"], 3)

        res = self.client.post("/api/equacao/segundo-grau", json={"a": 1, "b": -5, "c": 6})
        self.assertEqual(res.status_code, 200)
        dados = json.loads(res.data)["dados"]
        self.assertEqual(dados["tipo"], "duas_reais")
        self.assertEqual(dados["x1"], 3)
        self.assertEqual(dados["x2"], 2)

    def test_api_estatistica(self):
        """Testa endpoint de estatística."""
        res = self.client.post("/api/estatistica", json={"valores": "10, 20, 30"})
        self.assertEqual(res.status_code, 200)
        est = json.loads(res.data)["estatisticas"]
        self.assertEqual(est["media"], 20)
        self.assertEqual(est["mediana"], 20)
        self.assertEqual(est["maior"], 30)
        self.assertEqual(est["menor"], 10)

    def test_api_conversoes(self):
        """Testa conversões de unidades."""
        res = self.client.post("/api/conversao", json={"tipo": "celsius_fahrenheit", "valor": 0})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)["resultado"], 32)

        res = self.client.post("/api/conversao", json={"tipo": "km_m", "valor": 2.5})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)["resultado"], 2500)


if __name__ == "__main__":
    unittest.main()
