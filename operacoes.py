"""
Módulo de operações matemáticas da Calculadora Científica.
Cada função é responsável por uma única operação matemática pura e reutilizável.
Utiliza apenas a biblioteca nativa 'math' do Python.
Compatível com todos os terminais e encodings do Windows (CP1252, UTF-8).
"""

import math
from typing import List, Dict, Any, Union


# =============================================================================
# 1. OPERAÇÕES BÁSICAS
# =============================================================================

def adicionar(a: float, b: float) -> float:
    """Retorna a soma de a e b."""
    return a + b


def subtrair(a: float, b: float) -> float:
    """Retorna a diferença entre a e b."""
    return a - b


def multiplicar(a: float, b: float) -> float:
    """Retorna o produto de a e b."""
    return a * b


def dividir(a: float, b: float) -> float:
    """
    Retorna a divisão de a por b.
    Lança um ValueError caso o divisor seja zero.
    """
    if b == 0:
        raise ValueError("Divisão por zero não é permitida.")
    return a / b


# =============================================================================
# 2. PORCENTAGEM
# =============================================================================

def porcentagem_de_valor(percentual: float, valor: float) -> float:
    """
    Calcula a porcentagem de um valor.
    Exemplo: 20% de 150 = 30.0
    """
    return (percentual * valor) / 100.0


def aumento_percentual(valor: float, percentual: float) -> float:
    """
    Calcula o valor resultante após a aplicação de um aumento percentual.
    Exemplo: 100 com aumento de 15% = 115.0
    """
    return valor * (1.0 + (percentual / 100.0))


def desconto_percentual(valor: float, percentual: float) -> float:
    """
    Calcula o valor resultante após a aplicação de um desconto percentual.
    Exemplo: 100 com desconto de 15% = 85.0
    """
    return valor * (1.0 - (percentual / 100.0))


# =============================================================================
# 3. POTENCIAÇÃO E RADICIAÇÃO
# =============================================================================

def potencia(base: float, expoente: float) -> float:
    """
    Calcula a base elevada ao expoente (base^expoente).
    Trata erros de divisão por zero (0 com expoente negativo),
    raízes pares de bases negativas no conjunto dos reais e overflow.
    """
    if base == 0 and expoente < 0:
        raise ValueError("Não é possível elevar zero a um expoente negativo (divisão por zero).")

    # Base negativa com expoente fracionário gera número complexo
    if base < 0 and not float(expoente).is_integer():
        raise ValueError("Não é possível calcular potência de base negativa com expoente fracionário no conjunto dos reais.")

    try:
        return float(base ** expoente)
    except OverflowError:
        raise ValueError("Resultado excessivamente grande para a capacidade numérica (estouro de precisão).")


def raiz_quadrada(radicando: float) -> float:
    """
    Calcula a raiz quadrada de um número.
    Lança ValueError caso o radicando seja negativo.
    """
    if radicando < 0:
        raise ValueError("Não existe raiz quadrada real de número negativo.")
    return math.sqrt(radicando)


def raiz_enesima(radicando: float, indice: float) -> float:
    """
    Calcula a raiz de índice qualquer (n-ésima raiz de radicando).
    - Lança ValueError se o índice for igual a zero.
    - Se o radicando for negativo, calcula a raiz real se o índice for inteiro ímpar,
      ou lança ValueError se o índice for par ou fracionário.
    """
    if indice == 0:
        raise ValueError("O índice da raiz não pode ser zero.")

    if radicando == 0:
        if indice < 0:
            raise ValueError("Não é possível calcular raiz de zero com índice negativo (divisão por zero).")
        return 0.0

    if radicando > 0:
        return float(radicando ** (1.0 / indice))

    # Radicando negativo
    if float(indice).is_integer() and int(indice) % 2 != 0:
        # Raiz real com índice ímpar (ex: raiz cúbica de -8 é -2)
        return float(- (abs(radicando) ** (1.0 / indice)))
    else:
        raise ValueError("Não existe raiz real de número negativo com índice par ou fracionário.")


# =============================================================================
# 4. FUNÇÕES CIENTÍFICAS
# =============================================================================

def seno(angulo: float, em_graus: bool = True) -> float:
    """
    Calcula o seno de um ângulo.
    O parâmetro em_graus indica se o ângulo foi fornecido em graus (True) ou radianos (False).
    """
    rad = math.radians(angulo) if em_graus else angulo
    res = math.sin(rad)
    return 0.0 if math.isclose(res, 0.0, abs_tol=1e-12) else res


def cosseno(angulo: float, em_graus: bool = True) -> float:
    """
    Calcula o cosseno de um ângulo.
    O parâmetro em_graus indica se o ângulo foi fornecido em graus (True) ou radianos (False).
    """
    rad = math.radians(angulo) if em_graus else angulo
    res = math.cos(rad)
    return 0.0 if math.isclose(res, 0.0, abs_tol=1e-12) else res


def tangente(angulo: float, em_graus: bool = True) -> float:
    """
    Calcula a tangente de um ângulo.
    Lança ValueError se o ângulo tiver tangente indefinida (quando o cosseno for zero, ex: 90 graus).
    """
    rad = math.radians(angulo) if em_graus else angulo
    cos_val = math.cos(rad)
    if math.isclose(cos_val, 0.0, abs_tol=1e-12):
        unidade = "graus" if em_graus else "radianos"
        raise ValueError(f"Tangente indefinida para o ângulo {angulo} {unidade} (cosseno igual a zero).")
    res = math.tan(rad)
    return 0.0 if math.isclose(res, 0.0, abs_tol=1e-12) else res


def logaritmo_natural(x: float) -> float:
    """
    Calcula o logaritmo natural (ln) de x na base e.
    Lança ValueError se x <= 0.
    """
    if x <= 0:
        raise ValueError("O logaritmo natural (ln) é indefinido para valores menores ou iguais a zero.")
    return math.log(x)


def logaritmo_base10(x: float) -> float:
    """
    Calcula o logaritmo de x na base 10 (log10).
    Lança ValueError se x <= 0.
    """
    if x <= 0:
        raise ValueError("O logaritmo na base 10 (log) é indefinido para valores menores ou iguais a zero.")
    return math.log10(x)


def fatorial(n: Union[int, float]) -> int:
    """
    Calcula o fatorial de um número inteiro não negativo (n!).
    Lança ValueError para números negativos ou com parte fracionária.
    """
    if not isinstance(n, int):
        if not float(n).is_integer():
            raise ValueError("O fatorial só é definido para números inteiros.")
        n = int(n)

    if n < 0:
        raise ValueError("O fatorial não é definido para números negativos.")

    if n > 1000:
        raise ValueError("Valor excessivamente grande para o cálculo de fatorial (limite: 1000).")

    return math.factorial(n)


# =============================================================================
# 5. EQUAÇÕES (1º E 2º GRAU)
# =============================================================================

def resolver_equacao_primeiro_grau(a: float, b: float) -> Dict[str, Any]:
    """
    Resolve a equação linear ax + b = 0.
    Retorna o tipo de solução ('unica', 'infinitas' ou 'impossivel'), a raiz e uma explicação passo a passo.
    """
    if a == 0:
        if b == 0:
            return {
                "tipo": "infinitas",
                "solucao": None,
                "explicacao": "A equação 0x + 0 = 0 é indeterminada e possui infinitas soluções (qualquer número real satisfaz a equação)."
            }
        else:
            return {
                "tipo": "impossivel",
                "solucao": None,
                "explicacao": f"A equação 0x + ({b}) = 0 é impossível, pois 0 não pode ser igual a {-b}. Não existe solução real."
            }

    x = -b / a
    explicacao = (
        f"Equação: {a}x + ({b}) = 0\n"
        f"1. Isolar o termo com incógnita: {a}x = {-b}\n"
        f"2. Dividir ambos os lados por {a}: x = {-b} / {a}\n"
        f"Resultado: x = {x}"
    )
    return {
        "tipo": "unica",
        "solucao": x,
        "explicacao": explicacao
    }


def resolver_equacao_segundo_grau(a: float, b: float, c: float) -> Dict[str, Any]:
    """
    Resolve a equação quadrática ax^2 + bx + c = 0 via fórmula de Bhaskara.
    Retorna o tipo de solução, o valor de delta, as raízes e a explicação passo a passo.
    """
    if a == 0:
        res = resolver_equacao_primeiro_grau(b, c)
        res["explicacao"] = (
            "Como o coeficiente 'a' é igual a 0, esta é uma equação de 1º grau (bx + c = 0):\n"
            + res["explicacao"]
        )
        return res

    delta = (b ** 2) - (4 * a * c)

    if delta > 0:
        raiz_delta = math.sqrt(delta)
        x1 = (-b + raiz_delta) / (2 * a)
        x2 = (-b - raiz_delta) / (2 * a)
        explicacao = (
            f"Equação: {a}x^2 + ({b})x + ({c}) = 0\n"
            f"1. Discriminante (Delta = b^2 - 4ac):\n"
            f"   Delta = ({b})^2 - 4 * ({a}) * ({c}) = {delta}\n"
            f"2. Como Delta > 0 ({delta}), a equação possui duas raízes reais e distintas:\n"
            f"   x1 = (-({b}) + raiz({delta})) / (2 * {a}) = {x1}\n"
            f"   x2 = (-({b}) - raiz({delta})) / (2 * {a}) = {x2}"
        )
        return {
            "tipo": "duas_reais",
            "delta": delta,
            "x1": x1,
            "x2": x2,
            "explicacao": explicacao
        }
    elif delta == 0:
        x = -b / (2 * a)
        explicacao = (
            f"Equação: {a}x^2 + ({b})x + ({c}) = 0\n"
            f"1. Discriminante (Delta = b^2 - 4ac):\n"
            f"   Delta = ({b})^2 - 4 * ({a}) * ({c}) = 0\n"
            f"2. Como Delta = 0, a equação possui uma única raiz real dupla:\n"
            f"   x = -({b}) / (2 * {a}) = {x}"
        )
        return {
            "tipo": "raiz_unica",
            "delta": delta,
            "x": x,
            "explicacao": explicacao
        }
    else:
        explicacao = (
            f"Equação: {a}x^2 + ({b})x + ({c}) = 0\n"
            f"1. Discriminante (Delta = b^2 - 4ac):\n"
            f"   Delta = ({b})^2 - 4 * ({a}) * ({c}) = {delta}\n"
            f"2. Como Delta < 0 ({delta}), não existe raiz quadrada de número negativo no conjunto dos números reais.\n"
            f"   Portanto, a equação não possui raízes reais."
        )
        return {
            "tipo": "sem_raizes_reais",
            "delta": delta,
            "x1": None,
            "x2": None,
            "explicacao": explicacao
        }


# =============================================================================
# 6. ESTATÍSTICA
# =============================================================================

def calcular_estatisticas(valores: List[float]) -> Dict[str, float]:
    """
    Calcula média, mediana, maior e menor valor de uma lista numérica.
    Lança ValueError se a lista estiver vazia.
    """
    if not valores:
        raise ValueError("A lista de valores não pode estar vazia.")

    n = len(valores)
    media = sum(valores) / n
    maior = max(valores)
    menor = min(valores)

    ordenados = sorted(valores)
    if n % 2 != 0:
        mediana = float(ordenados[n // 2])
    else:
        meio1 = ordenados[(n // 2) - 1]
        meio2 = ordenados[n // 2]
        mediana = (meio1 + meio2) / 2.0

    return {
        "quantidade": float(n),
        "media": media,
        "mediana": mediana,
        "maior": maior,
        "menor": menor
    }


# =============================================================================
# 7. CONVERSÕES DE UNIDADES
# =============================================================================

def celsius_para_fahrenheit(c: float) -> float:
    """Converte temperatura de graus Celsius (°C) para Fahrenheit (°F)."""
    return (c * 9.0 / 5.0) + 32.0


def fahrenheit_para_celsius(f: float) -> float:
    """Converte temperatura de Fahrenheit (°F) para graus Celsius (°C)."""
    return (f - 32.0) * 5.0 / 9.0


def quilometros_para_metros(km: float) -> float:
    """Converte distância de quilômetros (km) para metros (m)."""
    return km * 1000.0


def metros_para_quilometros(m: float) -> float:
    """Converte distância de metros (m) para quilômetros (km)."""
    return m / 1000.0


def horas_para_minutos(h: float) -> float:
    """Converte tempo de horas (h) para minutos (min)."""
    return h * 60.0


def minutos_para_horas(minutos: float) -> float:
    """Converte tempo de minutos (min) para horas (h)."""
    return minutos / 60.0
