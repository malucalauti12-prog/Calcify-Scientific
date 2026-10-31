"""
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


def obter_lista_numeros(mensagem: str) -> List[float]:
    """Solicita uma sequência de números separados por espaço ou vírgula."""
    while True:
        entrada = input(mensagem).strip()
        if not entrada:
            print("Entrada vazia! Por favor, digite pelo menos um número.")
            continue
        try:
            itens = entrada.replace(",", " ").split()
            return [float(x) for x in itens]
        except ValueError:
            print("Entrada inválida! Digite apenas números separados por espaço ou vírgula.")


# =============================================================================
# MENUS E TELAS
# =============================================================================

def exibir_menu():
    """Exibe as opções de operações disponíveis para o usuário."""
    print("\n" + "=" * 30)
    print("      CALCULADORA EM PYTHON")
    print("=" * 30)
    print("1  - Adição (+)")
    print("2  - Subtração (-)")
    print("3  - Multiplicação (*)")
    print("4  - Divisão (/)")
    print("5  - Porcentagem (%)")
    print("6  - Potenciação e Radiciação (x^y, raiz)")
    print("7  - Funções Científicas (sin, cos, ln, n!)")
    print("8  - Equações (1º e 2º Grau)")
    print("9  - Estatística (Média, Mediana, etc.)")
    print("10 - Conversões de Unidades")
    print("0  - Sair")
    print("=" * 30)


def executar_porcentagem():
    """Submenu para cálculos de porcentagem."""
    while True:
        print("\n" + "-" * 30)
        print("          PORCENTAGEM")
        print("-" * 30)
        print("1 - Porcentagem de um valor (X% de Y)")
        print("2 - Aumento percentual (Valor + X%)")
        print("3 - Desconto percentual (Valor - X%)")
        print("0 - Voltar ao menu principal")
        print("-" * 30)
        opcao = input("Escolha uma opção (0 a 3): ").strip()

        if opcao == "0":
            break

        if opcao not in ["1", "2", "3"]:
            print("\nOpção inválida! Escolha uma opção do menu.")
            continue

        try:
            if opcao == "1":
                pct = obter_numero("Digite a porcentagem (%): ")
                val = obter_numero("Digite o valor base: ")
                res = porcentagem_de_valor(pct, val)
                print(f"\nResultado: {pct}% de {val} = {res}")
            elif opcao == "2":
                val = obter_numero("Digite o valor inicial: ")
                pct = obter_numero("Digite a porcentagem de aumento (%): ")
                res = aumento_percentual(val, pct)
                print(f"\nResultado: {val} com {pct}% de aumento = {res}")
            elif opcao == "3":
                val = obter_numero("Digite o valor inicial: ")
                pct = obter_numero("Digite a porcentagem de desconto (%): ")
                res = desconto_percentual(val, pct)
                print(f"\nResultado: {val} com {pct}% de desconto = {res}")
        except ValueError as erro:
            print(f"\nErro no cálculo: {erro}")


def executar_potenciacao_radiciacao():
    """Submenu para potência e raízes."""
    while True:
        print("\n" + "-" * 30)
        print("    POTENCIAÇÃO E RADICIAÇÃO")
        print("-" * 30)
        print("1 - Potência (base ^ expoente)")
        print("2 - Raiz quadrada (raiz de x)")
        print("3 - Raiz de qualquer índice (n-ésima raiz)")
        print("0 - Voltar ao menu principal")
        print("-" * 30)
        opcao = input("Escolha uma opção (0 a 3): ").strip()

        if opcao == "0":
            break

        if opcao not in ["1", "2", "3"]:
            print("\nOpção inválida! Escolha uma opção do menu.")
            continue

        try:
            if opcao == "1":
                base = obter_numero("Digite a base: ")
                exp = obter_numero("Digite o expoente: ")
                res = potencia(base, exp)
                print(f"\nResultado: {base} ^ {exp} = {res}")
            elif opcao == "2":
                num = obter_numero("Digite o radicando (número dentro da raiz): ")
                res = raiz_quadrada(num)
                print(f"\nResultado: raiz({num}) = {res}")
            elif opcao == "3":
                rad = obter_numero("Digite o radicando: ")
                ind = obter_numero("Digite o índice da raiz (ex: 3 para cúbica): ")
                res = raiz_enesima(rad, ind)
                print(f"\nResultado: Raiz de índice {ind} de {rad} = {res}")
        except ValueError as erro:
            print(f"\nErro no cálculo: {erro}")


def executar_funcoes_cientificas():
    """Submenu para funções científicas (trigonometria, logaritmos, fatorial)."""
    while True:
        print("\n" + "-" * 30)
        print("      FUNÇÕES CIENTÍFICAS")
        print("-" * 30)
        print("1 - Seno (sin)")
        print("2 - Cosseno (cos)")
        print("3 - Tangente (tan)")
        print("4 - Logaritmo natural (ln)")
        print("5 - Logaritmo de base 10 (log10)")
        print("6 - Fatorial (n!)")
        print("0 - Voltar ao menu principal")
        print("-" * 30)
        opcao = input("Escolha uma opção (0 a 6): ").strip()

        if opcao == "0":
            break

        if opcao not in ["1", "2", "3", "4", "5", "6"]:
            print("\nOpção inválida! Escolha uma opção do menu.")
            continue

        try:
            if opcao in ["1", "2", "3"]:
                print("\nDefina a unidade do ângulo:")
                print("1 - Graus")
                print("2 - Radianos")
                u_opt = input("Escolha (1 para graus, 2 para radianos) [Padrão: 1]: ").strip()
                em_graus = (u_opt != "2")
                unidade_nome = "graus" if em_graus else "radianos"

                ang = obter_numero(f"Digite o ângulo em {unidade_nome}: ")

                if opcao == "1":
                    res = seno(ang, em_graus=em_graus)
                    print(f"\nResultado: sen({ang} {unidade_nome}) = {res}")
                elif opcao == "2":
                    res = cosseno(ang, em_graus=em_graus)
                    print(f"\nResultado: cos({ang} {unidade_nome}) = {res}")
                elif opcao == "3":
                    res = tangente(ang, em_graus=em_graus)
                    print(f"\nResultado: tan({ang} {unidade_nome}) = {res}")

            elif opcao == "4":
                val = obter_numero("Digite o valor para calcular ln(x): ")
                res = logaritmo_natural(val)
                print(f"\nResultado: ln({val}) = {res}")

            elif opcao == "5":
                val = obter_numero("Digite o valor para calcular log10(x): ")
                res = logaritmo_base10(val)
                print(f"\nResultado: log10({val}) = {res}")

            elif opcao == "6":
                n = obter_inteiro("Digite um número inteiro não negativo (ex: 5): ")
                res = fatorial(n)
                print(f"\nResultado: {n}! = {res}")

        except ValueError as erro:
            print(f"\nErro no cálculo: {erro}")


def executar_equacoes():
    """Submenu para resolução de equações de 1º e 2º grau."""
    while True:
        print("\n" + "-" * 30)
        print("      RESOLUÇÃO DE EQUAÇÕES")
        print("-" * 30)
        print("1 - Equação de 1º grau (ax + b = 0)")
        print("2 - Equação de 2º grau (ax^2 + bx + c = 0)")
        print("0 - Voltar ao menu principal")
        print("-" * 30)
        opcao = input("Escolha uma opção (0 a 2): ").strip()

        if opcao == "0":
            break

        if opcao not in ["1", "2"]:
            print("\nOpção inválida! Escolha uma opção do menu.")
            continue

        try:
            if opcao == "1":
                print("\nEquação no formato: ax + b = 0")
                a = obter_numero("Digite o coeficiente a: ")
                b = obter_numero("Digite o coeficiente b: ")
                resultado = resolver_equacao_primeiro_grau(a, b)
                print("\n--- Explicação do Cálculo ---")
                print(resultado["explicacao"])
                print("-----------------------------")

            elif opcao == "2":
                print("\nEquação no formato: ax^2 + bx + c = 0")
                a = obter_numero("Digite o coeficiente a: ")
                b = obter_numero("Digite o coeficiente b: ")
                c = obter_numero("Digite o coeficiente c: ")
                resultado = resolver_equacao_segundo_grau(a, b, c)
                print("\n--- Explicação do Cálculo ---")
                print(resultado["explicacao"])
                print("-----------------------------")

        except ValueError as erro:
            print(f"\nErro no cálculo: {erro}")


def executar_estatistica():
    """Submenu para cálculos estatísticos."""
    while True:
        print("\n" + "-" * 30)
        print("          ESTATÍSTICA")
        print("-" * 30)
        print("1 - Inserir lista de números (Média, Mediana, Maior e Menor)")
        print("0 - Voltar ao menu principal")
        print("-" * 30)
        opcao = input("Escolha uma opção (0 ou 1): ").strip()

        if opcao == "0":
            break

        if opcao != "1":
            print("\nOpção inválida! Escolha uma opção do menu.")
            continue

        try:
            valores = obter_lista_numeros("Digite os números separados por espaço ou vírgula: ")
            res = calcular_estatisticas(valores)

            print("\n" + "-" * 30)
            print("      RESUMO ESTATÍSTICO")
            print("-" * 30)
            print(f"Valores inseridos : {valores}")
            print(f"Total de elementos: {int(res['quantidade'])}")
            print(f"Média             : {res['media']}")
            print(f"Mediana           : {res['mediana']}")
            print(f"Maior valor       : {res['maior']}")
            print(f"Menor valor       : {res['menor']}")
            print("-" * 30)

        except ValueError as erro:
            print(f"\nErro no cálculo: {erro}")


def executar_conversoes():
    """Submenu para conversão de unidades de medida."""
    while True:
        print("\n" + "-" * 30)
        print("    CONVERSÕES DE UNIDADES")
        print("-" * 30)
        print("1 - Celsius (°C) para Fahrenheit (°F)")
        print("2 - Fahrenheit (°F) para Celsius (°C)")
        print("3 - Quilômetros (km) para Metros (m)")
        print("4 - Metros (m) para Quilômetros (km)")
        print("5 - Horas (h) para Minutos (min)")
        print("6 - Minutos (min) para Horas (h)")
        print("0 - Voltar ao menu principal")
        print("-" * 30)
        opcao = input("Escolha uma opção (0 a 6): ").strip()

        if opcao == "0":
            break

        if opcao not in ["1", "2", "3", "4", "5", "6"]:
            print("\nOpção inválida! Escolha uma opção do menu.")
            continue

        try:
            if opcao == "1":
                c = obter_numero("Digite a temperatura em Celsius (°C): ")
                res = celsius_para_fahrenheit(c)
                print(f"\nResultado: {c} °C = {res:.2f} °F")
            elif opcao == "2":
                f = obter_numero("Digite a temperatura em Fahrenheit (°F): ")
                res = fahrenheit_para_celsius(f)
                print(f"\nResultado: {f} °F = {res:.2f} °C")
            elif opcao == "3":
                km = obter_numero("Digite a distância em quilômetros (km): ")
                res = quilometros_para_metros(km)
                print(f"\nResultado: {km} km = {res} m")
            elif opcao == "4":
                m = obter_numero("Digite a distância em metros (m): ")
                res = metros_para_quilometros(m)
                print(f"\nResultado: {m} m = {res} km")
            elif opcao == "5":
                h = obter_numero("Digite o tempo em horas (h): ")
                res = horas_para_minutos(h)
                print(f"\nResultado: {h} h = {res} min")
            elif opcao == "6":
                m = obter_numero("Digite o tempo em minutos (min): ")
                res = minutos_para_horas(m)
                print(f"\nResultado: {m} min = {res} h")
        except ValueError as erro:
            print(f"\nErro no cálculo: {erro}")


# =============================================================================
# LOOP PRINCIPAL
# =============================================================================

def executar():
    """Loop principal que controla a execução da calculadora."""
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção (0 a 10): ").strip()

        if opcao == "0":
            print("\nObrigado por usar a calculadora! Até logo!")
            break

        if opcao not in [str(i) for i in range(11)]:
            print("\nOpção inválida! Escolha uma opção do menu.")
            continue

        # Operações Básicas originais (opções 1 a 4 preservadas integralmente)
        if opcao in ["1", "2", "3", "4"]:
            num1 = obter_numero("Digite o primeiro número: ")
            num2 = obter_numero("Digite o segundo número: ")

            try:
                if opcao == "1":
                    resultado = adicionar(num1, num2)
                    simbolo = "+"
                elif opcao == "2":
                    resultado = subtrair(num1, num2)
                    simbolo = "-"
                elif opcao == "3":
                    resultado = multiplicar(num1, num2)
                    simbolo = "*"
                elif opcao == "4":
                    resultado = dividir(num1, num2)
                    simbolo = "/"

                print(f"\nResultado: {num1} {simbolo} {num2} = {resultado}")

            except ValueError as erro:
                print(f"\nErro no cálculo: {erro}")

        # Novas funcionalidades científicas
        elif opcao == "5":
            executar_porcentagem()
        elif opcao == "6":
            executar_potenciacao_radiciacao()
        elif opcao == "7":
            executar_funcoes_cientificas()
        elif opcao == "8":
            executar_equacoes()
        elif opcao == "9":
            executar_estatistica()
        elif opcao == "10":
            executar_conversoes()


if __name__ == "__main__":
    executar()
