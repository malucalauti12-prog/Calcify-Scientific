"""
Aplicação Web Calcify - Backend em Flask.
Conecta a interface web moderna às funções matemáticas puras de operacoes.py.
Preparado para execução local e deploy no Render com Gunicorn.
"""

import os
from jinja2 import ChoiceLoader, FileSystemLoader
from flask import Flask, render_template, request, jsonify, send_from_directory
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

# Diretório base absoluto onde está app.py (evita falhas de CWD no Render/Gunicorn)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configuração explícita de pastas
template_dir_padrao = os.path.join(BASE_DIR, "templates")
static_dir_padrao = os.path.join(BASE_DIR, "static")

app = Flask(
    __name__,
    template_folder=template_dir_padrao,
    static_folder=static_dir_padrao,
    static_url_path="/static"
)

# Carregador multi-diretório resiliente (evita TemplateNotFound em qualquer estrutura no Render)
candidatos_templates = [
    template_dir_padrao,                                    # 1. /templates (padrão)
    os.path.join(BASE_DIR, "Templates"),                    # 2. /Templates (caso o usuário tenha criado com T maiúsculo)
    BASE_DIR,                                               # 3. Raiz do projeto (caso index.html esteja na raiz)
    os.path.join(os.getcwd(), "templates"),                 # 4. templates relativo ao CWD do Render
    os.path.join(os.getcwd(), "Templates"),                 # 5. Templates relativo ao CWD do Render
    os.path.join(os.getcwd(), "calculadora", "templates"),  # 6. Se o repositório tiver subpasta calculadora
    os.path.join(os.getcwd(), "calculadora"),               # 7. Subpasta calculadora raiz
    os.getcwd()                                             # 8. CWD do Render
]

app.jinja_loader = ChoiceLoader([
    FileSystemLoader(p) for p in candidatos_templates if os.path.isdir(p)
])


# =============================================================================
# ROTAS DE PÁGINAS E FALLBACKS ESTÁTICOS
# =============================================================================

@app.route("/")
def index():
    """Renderiza a página principal do Calcify."""
    return render_template("index.html")


@app.route("/style.css")
def root_style():
    """Rota de contingência caso o navegador solicite style.css na raiz."""
    css_path = os.path.join(BASE_DIR, "static", "css")
    if os.path.exists(os.path.join(css_path, "style.css")):
        return send_from_directory(css_path, "style.css")
    return send_from_directory(BASE_DIR, "style.css")


@app.route("/main.js")
def root_js():
    """Rota de contingência caso o navegador solicite main.js na raiz."""
    js_path = os.path.join(BASE_DIR, "static", "js")
    if os.path.exists(os.path.join(js_path, "main.js")):
        return send_from_directory(js_path, "main.js")
    return send_from_directory(BASE_DIR, "main.js")


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
