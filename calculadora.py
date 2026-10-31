""
Interface principal da Calculadora Científica em Python.
Responsável por interagir com o usuário via terminal.
Preserva integralmente a estrutura e estilo originais do projeto.
"""
from typing import List
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
def obter_numero(mensagem: str) -> float:
    """Solicita um número ao usuário e garante que o valor digitado seja válido."""
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print("Entrada inválida! Por favor, digite um número válido.")
def obter_inteiro(mensagem: str) -> int:
    """Solicita um número inteiro ao usuário e garante validação."""
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Entrada inválida! Por favor, digite um número inteiro.")
