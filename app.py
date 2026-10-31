"""
Aplicação Web Calcify - Backend em Flask.
Conecta a interface web moderna às funções matemáticas puras de operacoes.py.
Preparado para execução local e deploy no Render com Gunicorn.
"""

import os
from flask import Flask, render_template, request, jsonify
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

app = Flask(__name__)


# =============================================================================
# ROTAS DE PÁGINAS
# =============================================================================

@app.route("/")
def index():
    """Renderiza a página principal do Calcify."""
    return render_template("index.html")


@app.route("/api/status", methods=["GET"])
def status():
    """Retorna o status da aplicação para monitoramento e health check."""
    return jsonify({
        "status": "online",
        "aplicacao": "Calcify",
        "versao": "2.0.0",
        "slogan": "Make numbers simple."
    })


# =============================================================================
# API: OPERAÇÕES DA CALCULADORA BÁSICA E CIENTÍFICA
# =============================================================================

@app.route("/api/calcular", methods=["POST"])
def calcular():
    """
    Executa uma operação matemática recebendo JSON.
    Formato esperado: { "operacao": "...", ...parametros }
    """
    dados = request.get_json(silent=True) or {}
    operacao = dados.get("operacao")

    if not operacao:
        return jsonify({"success": False, "error": "Operação não especificada."}), 400

    try:
        resultado = None

        # 1. Operações Básicas
        if operacao == "adicionar":
            a = float(dados["a"])
            b = float(dados["b"])
            resultado = adicionar(a, b)

        elif operacao == "subtrair":
            a = float(dados["a"])
            b = float(dados["b"])
            resultado = subtrair(a, b)

        elif operacao == "multiplicar":
            a = float(dados["a"])
            b = float(dados["b"])
            resultado = multiplicar(a, b)

        elif operacao == "dividir":
            a = float(dados["a"])
            b = float(dados["b"])
            resultado = dividir(a, b)

        # 2. Porcentagem
        elif operacao == "porcentagem_de_valor":
            percentual = float(dados["percentual"])
            valor = float(dados["valor"])
            resultado = porcentagem_de_valor(percentual, valor)

        elif operacao == "aumento_percentual":
            valor = float(dados["valor"])
            percentual = float(dados["percentual"])
            resultado = aumento_percentual(valor, percentual)

        elif operacao == "desconto_percentual":
            valor = float(dados["valor"])
            percentual = float(dados["percentual"])
            resultado = desconto_percentual(valor, percentual)

        # 3. Potenciação e Radiciação
        elif operacao == "potencia":
            base = float(dados["base"])
            expoente = float(dados["expoente"])
            resultado = potencia(base, expoente)

        elif operacao == "raiz_quadrada":
            radicando = float(dados["radicando"])
            resultado = raiz_quadrada(radicando)

        elif operacao == "raiz_enesima":
            radicando = float(dados["radicando"])
            indice = float(dados["indice"])
            resultado = raiz_enesima(radicando, indice)

        # 4. Funções Científicas
        elif operacao == "seno":
            angulo = float(dados["angulo"])
            em_graus = bool(dados.get("em_graus", True))
            resultado = seno(angulo, em_graus=em_graus)

        elif operacao == "cosseno":
            angulo = float(dados["angulo"])
            em_graus = bool(dados.get("em_graus", True))
            resultado = cosseno(angulo, em_graus=em_graus)

        elif operacao == "tangente":
            angulo = float(dados["angulo"])
            em_graus = bool(dados.get("em_graus", True))
            resultado = tangente(angulo, em_graus=em_graus)

        elif operacao == "logaritmo_natural":
            x = float(dados["x"])
            resultado = logaritmo_natural(x)

        elif operacao == "logaritmo_base10":
            x = float(dados["x"])
            resultado = logaritmo_base10(x)

        elif operacao == "fatorial":
            n = dados["n"]
            resultado = fatorial(n)

        else:
            return jsonify({"success": False, "error": f"Operação '{operacao}' não reconhecida."}), 400

        # Formata resultado caso seja float exato ou inteiro eliminando resíduo de ponto flutuante
        if isinstance(resultado, float):
            resultado = round(resultado, 12)
            if resultado.is_integer():
                resultado_formatado = int(resultado)
            else:
                resultado_formatado = resultado
        else:
            resultado_formatado = resultado

        return jsonify({
            "success": True,
            "operacao": operacao,
            "resultado": resultado_formatado
        })

    except KeyError as e:
        return jsonify({"success": False, "error": f"Parâmetro obrigatório ausente: {str(e)}"}), 400
    except (ValueError, ZeroDivisionError) as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"Erro interno no cálculo: {str(e)}"}), 500


# =============================================================================
# API: EQUAÇÕES
# =============================================================================

@app.route("/api/equacao/primeiro-grau", methods=["POST"])
def equacao_primeiro_grau():
    """Resolve equação linear ax + b = 0."""
    dados = request.get_json(silent=True) or {}
    try:
        a = float(dados["a"])
        b = float(dados["b"])
        resposta = resolver_equacao_primeiro_grau(a, b)
        return jsonify({"success": True, "dados": resposta})
    except KeyError as e:
        return jsonify({"success": False, "error": f"Parâmetro ausente: {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/equacao/segundo-grau", methods=["POST"])
def equacao_segundo_grau():
    """Resolve equação quadrática ax² + bx + c = 0."""
    dados = request.get_json(silent=True) or {}
    try:
        a = float(dados["a"])
        b = float(dados["b"])
        c = float(dados["c"])
        resposta = resolver_equacao_segundo_grau(a, b, c)
        return jsonify({"success": True, "dados": resposta})
    except KeyError as e:
        return jsonify({"success": False, "error": f"Parâmetro ausente: {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400


# =============================================================================
# API: ESTATÍSTICA
# =============================================================================

@app.route("/api/estatistica", methods=["POST"])
def estatistica():
    """Calcula estatísticas de uma lista de números."""
    dados = request.get_json(silent=True) or {}
    valores_brutos = dados.get("valores")

    if valores_brutos is None:
        return jsonify({"success": False, "error": "Campo 'valores' é obrigatório."}), 400

    try:
        if isinstance(valores_brutos, str):
            # Converte texto separado por vírgula ou espaço em lista de floats
            itens = valores_brutos.replace(",", " ").split()
            valores = [float(x) for x in itens]
        elif isinstance(valores_brutos, list):
            valores = [float(x) for x in valores_brutos]
        else:
            return jsonify({"success": False, "error": "Formato de valores inválido."}), 400

        resultado = calcular_estatisticas(valores)
        return jsonify({"success": True, "estatisticas": resultado})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400


# =============================================================================
# API: CONVERSÕES DE UNIDADES
# =============================================================================

@app.route("/api/conversao", methods=["POST"])
def conversao():
    """Realiza conversões de temperatura, distância e tempo."""
    dados = request.get_json(silent=True) or {}
    tipo = dados.get("tipo")
    valor = dados.get("valor")

    if tipo is None or valor is None:
        return jsonify({"success": False, "error": "Campos 'tipo' e 'valor' são obrigatórios."}), 400

    try:
        val = float(valor)
        if tipo == "celsius_fahrenheit":
            res = celsius_para_fahrenheit(val)
            unidade_origem, unidade_destino = "°C", "°F"
        elif tipo == "fahrenheit_celsius":
            res = fahrenheit_para_celsius(val)
            unidade_origem, unidade_destino = "°F", "°C"
        elif tipo == "km_m":
            res = quilometros_para_metros(val)
            unidade_origem, unidade_destino = "km", "m"
        elif tipo == "m_km":
            res = metros_para_quilometros(val)
            unidade_origem, unidade_destino = "m", "km"
        elif tipo == "horas_minutos":
            res = horas_para_minutos(val)
            unidade_origem, unidade_destino = "h", "min"
        elif tipo == "minutos_horas":
            res = minutos_para_horas(val)
            unidade_origem, unidade_destino = "min", "h"
        else:
            return jsonify({"success": False, "error": f"Tipo de conversão '{tipo}' não suportado."}), 400

        return jsonify({
            "success": True,
            "tipo": tipo,
            "entrada": val,
            "unidade_origem": unidade_origem,
            "resultado": res,
            "unidade_destino": unidade_destino
        })
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400


# =============================================================================
# INICIALIZAÇÃO LOCAL E RENDER
# =============================================================================

if __name__ == "__main__":
    # Permite porta dinâmica para compatibilidade com Render ou porta 5000 local
    porta = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=porta, debug=True)
