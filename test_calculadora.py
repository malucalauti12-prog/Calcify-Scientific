"""
Testes unitários para as operações da calculadora científica.
Utiliza o framework padrão do Python: unittest.
Testa todas as operações novas e antigas, incluindo casos extremos e entradas inválidas.
"""

import math
import unittest
from operacoes import (
    adicionar,
    subtrair,
    multiplicar,
    dividir,
    porcentagem_de_valor,
    aumento_percentual,
    desconto_percentual,
    potencia,
    raiz_quadrada,
    raiz_enesima,
    seno,
    cosseno,
    tangente,
    logaritmo_natural,
    logaritmo_base10,
    fatorial,
    resolver_equacao_primeiro_grau,
    resolver_equacao_segundo_grau,
    calcular_estatisticas,
    celsius_para_fahrenheit,
    fahrenheit_para_celsius,
    quilometros_para_metros,
    metros_para_quilometros,
    horas_para_minutos,
    minutos_para_horas,
)


class TestOperacoesBasicas(unittest.TestCase):
    """Testes para as operações matemáticas básicas (+, -, *, /)."""

    def test_adicionar(self):
        self.assertEqual(adicionar(5, 3), 8)
        self.assertEqual(adicionar(-2, 5), 3)
        self.assertEqual(adicionar(0, 0), 0)
        self.assertAlmostEqual(adicionar(1.2, 3.4), 4.6)

    def test_subtrair(self):
        self.assertEqual(subtrair(10, 4), 6)
        self.assertEqual(subtrair(5, 10), -5)
        self.assertEqual(subtrair(0, 7), -7)
        self.assertAlmostEqual(subtrair(5.5, 2.2), 3.3)

    def test_multiplicar(self):
        self.assertEqual(multiplicar(3, 4), 12)
        self.assertEqual(multiplicar(-2, 3), -6)
        self.assertEqual(multiplicar(5, 0), 0)
        self.assertAlmostEqual(multiplicar(2.5, 4.0), 10.0)

    def test_dividir(self):
        self.assertEqual(dividir(10, 2), 5)
        self.assertEqual(dividir(9, 2), 4.5)
        self.assertEqual(dividir(-8, 2), -4)

    def test_dividir_por_zero(self):
        with self.assertRaises(ValueError):
            dividir(10, 0)
        with self.assertRaises(ValueError):
            dividir(0, 0)


class TestPorcentagem(unittest.TestCase):
    """Testes para cálculos de porcentagem, aumento e desconto percentual."""

    def test_porcentagem_de_valor(self):
        self.assertAlmostEqual(porcentagem_de_valor(20, 150), 30.0)
        self.assertAlmostEqual(porcentagem_de_valor(0, 100), 0.0)
        self.assertAlmostEqual(porcentagem_de_valor(150, 200), 300.0)

    def test_aumento_percentual(self):
        self.assertAlmostEqual(aumento_percentual(100, 15), 115.0)
        self.assertAlmostEqual(aumento_percentual(200, 0), 200.0)
        self.assertAlmostEqual(aumento_percentual(50, 100), 100.0)

    def test_desconto_percentual(self):
        self.assertAlmostEqual(desconto_percentual(100, 15), 85.0)
        self.assertAlmostEqual(desconto_percentual(200, 0), 200.0)
        self.assertAlmostEqual(desconto_percentual(50, 100), 0.0)


class TestPotenciacaoERadiciacao(unittest.TestCase):
    """Testes para potência, raiz quadrada e raiz de qualquer índice."""

    def test_potencia(self):
        self.assertEqual(potencia(2, 3), 8)
        self.assertEqual(potencia(5, 0), 1)
        self.assertEqual(potencia(-2, 3), -8)
        self.assertEqual(potencia(-2, 2), 4)
        self.assertEqual(potencia(0, 5), 0)
        self.assertAlmostEqual(potencia(4, 0.5), 2.0)

    def test_potencia_casos_invalidos(self):
        # 0 elevado a expoente negativo é divisão por zero
        with self.assertRaises(ValueError):
            potencia(0, -2)
        # Base negativa com expoente fracionário gera número complexo
        with self.assertRaises(ValueError):
            potencia(-4, 0.5)

    def test_raiz_quadrada(self):
        self.assertAlmostEqual(raiz_quadrada(9), 3.0)
        self.assertAlmostEqual(raiz_quadrada(0), 0.0)
        self.assertAlmostEqual(raiz_quadrada(2.25), 1.5)

    def test_raiz_quadrada_negativo(self):
        with self.assertRaises(ValueError):
            raiz_quadrada(-9)

    def test_raiz_enesima(self):
        # Raiz cúbica de 27 é 3
        self.assertAlmostEqual(raiz_enesima(27, 3), 3.0)
        # Raiz quarta de 16 é 2
        self.assertAlmostEqual(raiz_enesima(16, 4), 2.0)
        # Raiz de zero
        self.assertEqual(raiz_enesima(0, 3), 0.0)
        # Raiz de radicando negativo com índice ímpar no conjunto dos reais
        self.assertAlmostEqual(raiz_enesima(-8, 3), -2.0)
        self.assertAlmostEqual(raiz_enesima(-32, 5), -2.0)

    def test_raiz_enesima_invalidas(self):
        # Índice zero
        with self.assertRaises(ValueError):
            raiz_enesima(16, 0)
        # Radicando negativo com índice par
        with self.assertRaises(ValueError):
            raiz_enesima(-16, 2)
        # Radicando zero com índice negativo
        with self.assertRaises(ValueError):
            raiz_enesima(0, -3)


class TestFuncoesCientificas(unittest.TestCase):
    """Testes para seno, cosseno, tangente, logaritmos e fatorial."""

    def test_trigonometria_graus(self):
        self.assertAlmostEqual(seno(0, em_graus=True), 0.0)
        self.assertAlmostEqual(seno(90, em_graus=True), 1.0)
        self.assertAlmostEqual(seno(180, em_graus=True), 0.0)

        self.assertAlmostEqual(cosseno(0, em_graus=True), 1.0)
        self.assertAlmostEqual(cosseno(90, em_graus=True), 0.0)
        self.assertAlmostEqual(cosseno(180, em_graus=True), -1.0)

        self.assertAlmostEqual(tangente(0, em_graus=True), 0.0)
        self.assertAlmostEqual(tangente(45, em_graus=True), 1.0)

    def test_trigonometria_radianos(self):
        self.assertAlmostEqual(seno(math.pi / 2, em_graus=False), 1.0)
        self.assertAlmostEqual(cosseno(math.pi, em_graus=False), -1.0)
        self.assertAlmostEqual(tangente(0, em_graus=False), 0.0)

    def test_tangente_indefinida(self):
        # Tangente de 90° e 270° não é definida
        with self.assertRaises(ValueError):
            tangente(90, em_graus=True)
        with self.assertRaises(ValueError):
            tangente(270, em_graus=True)
        with self.assertRaises(ValueError):
            tangente(math.pi / 2, em_graus=False)

    def test_logaritmo_natural(self):
        self.assertAlmostEqual(logaritmo_natural(math.e), 1.0)
        self.assertAlmostEqual(logaritmo_natural(1), 0.0)
        # x <= 0 é indefinido
        with self.assertRaises(ValueError):
            logaritmo_natural(0)
        with self.assertRaises(ValueError):
            logaritmo_natural(-5)

    def test_logaritmo_base10(self):
        self.assertAlmostEqual(logaritmo_base10(100), 2.0)
        self.assertAlmostEqual(logaritmo_base10(10), 1.0)
        self.assertAlmostEqual(logaritmo_base10(1), 0.0)
        # x <= 0 é indefinido
        with self.assertRaises(ValueError):
            logaritmo_base10(0)
        with self.assertRaises(ValueError):
            logaritmo_base10(-10)

    def test_fatorial(self):
        self.assertEqual(fatorial(0), 1)
        self.assertEqual(fatorial(1), 1)
        self.assertEqual(fatorial(5), 120)
        self.assertEqual(fatorial(7), 5040)
        self.assertEqual(fatorial(4.0), 24)  # float com valor inteiro é aceito

    def test_fatorial_invalido(self):
        with self.assertRaises(ValueError):
            fatorial(-1)
        with self.assertRaises(ValueError):
            fatorial(3.5)


class TestEquacoes(unittest.TestCase):
    """Testes para resolução de equações de 1º e 2º grau."""

    def test_equacao_primeiro_grau(self):
        # 2x - 4 = 0 -> x = 2
        res1 = resolver_equacao_primeiro_grau(2, -4)
        self.assertEqual(res1["tipo"], "unica")
        self.assertAlmostEqual(res1["solucao"], 2.0)

        # 0x + 0 = 0 -> infinitas soluções
        res2 = resolver_equacao_primeiro_grau(0, 0)
        self.assertEqual(res2["tipo"], "infinitas")

        # 0x + 5 = 0 -> impossível
        res3 = resolver_equacao_primeiro_grau(0, 5)
        self.assertEqual(res3["tipo"], "impossivel")

    def test_equacao_segundo_grau_duas_raizes(self):
        # x² - 5x + 6 = 0 -> raízes 3 e 2
        res = resolver_equacao_segundo_grau(1, -5, 6)
        self.assertEqual(res["tipo"], "duas_reais")
        self.assertEqual(res["delta"], 1)
        self.assertAlmostEqual(res["x1"], 3.0)
        self.assertAlmostEqual(res["x2"], 2.0)

    def test_equacao_segundo_grau_raiz_unica(self):
        # x² - 4x + 4 = 0 -> delta = 0, raiz única 2
        res = resolver_equacao_segundo_grau(1, -4, 4)
        self.assertEqual(res["tipo"], "raiz_unica")
        self.assertEqual(res["delta"], 0)
        self.assertAlmostEqual(res["x"], 2.0)

    def test_equacao_segundo_grau_sem_raizes_reais(self):
        # x² + 0x + 4 = 0 -> delta = -16 < 0
        res = resolver_equacao_segundo_grau(1, 0, 4)
        self.assertEqual(res["tipo"], "sem_raizes_reais")
        self.assertLess(res["delta"], 0)
        self.assertIsNone(res["x1"])

    def test_equacao_segundo_grau_com_a_zero(self):
        # a = 0 -> reduz a 1º grau (2x + 4 = 0 -> x = -2)
        res = resolver_equacao_segundo_grau(0, 2, 4)
        self.assertEqual(res["tipo"], "unica")
        self.assertAlmostEqual(res["solucao"], -2.0)


class TestEstatistica(unittest.TestCase):
    """Testes para estatística (média, mediana, maior, menor)."""

    def test_estatistica_lista_impar(self):
        dados = [10.0, 20.0, 30.0]
        res = calcular_estatisticas(dados)
        self.assertEqual(res["quantidade"], 3)
        self.assertAlmostEqual(res["media"], 20.0)
        self.assertAlmostEqual(res["mediana"], 20.0)
        self.assertEqual(res["maior"], 30.0)
        self.assertEqual(res["menor"], 10.0)

    def test_estatistica_lista_par(self):
        dados = [1.0, 2.0, 3.0, 4.0]
        res = calcular_estatisticas(dados)
        self.assertEqual(res["quantidade"], 4)
        self.assertAlmostEqual(res["media"], 2.5)
        self.assertAlmostEqual(res["mediana"], 2.5)
        self.assertEqual(res["maior"], 4.0)
        self.assertEqual(res["menor"], 1.0)

    def test_estatistica_lista_vazia(self):
        with self.assertRaises(ValueError):
            calcular_estatisticas([])


class TestConversoes(unittest.TestCase):
    """Testes para conversão de temperaturas, distâncias e tempos."""

    def test_celsius_fahrenheit(self):
        self.assertAlmostEqual(celsius_para_fahrenheit(0), 32.0)
        self.assertAlmostEqual(celsius_para_fahrenheit(100), 212.0)
        self.assertAlmostEqual(celsius_para_fahrenheit(-40), -40.0)

        self.assertAlmostEqual(fahrenheit_para_celsius(32), 0.0)
        self.assertAlmostEqual(fahrenheit_para_celsius(212), 100.0)
        self.assertAlmostEqual(fahrenheit_para_celsius(-40), -40.0)

    def test_quilometros_metros(self):
        self.assertAlmostEqual(quilometros_para_metros(1), 1000.0)
        self.assertAlmostEqual(quilometros_para_metros(2.5), 2500.0)
        self.assertAlmostEqual(metros_para_quilometros(1000), 1.0)
        self.assertAlmostEqual(metros_para_quilometros(250), 0.25)

    def test_horas_minutos(self):
        self.assertAlmostEqual(horas_para_minutos(1), 60.0)
        self.assertAlmostEqual(horas_para_minutos(2.5), 150.0)
        self.assertAlmostEqual(minutos_para_horas(60), 1.0)
        self.assertAlmostEqual(minutos_para_horas(90), 1.5)


if __name__ == "__main__":
    unittest.main()
