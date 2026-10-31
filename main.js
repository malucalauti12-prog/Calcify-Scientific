/**
 * CALCIFY - LÓGICA DO FRONTEND INTERATIVO
 * Integra a interface moderna com as APIs do Flask (operacoes.py).
 */

document.addEventListener("DOMContentLoaded", () => {
  // ===========================================================================
  // 1. TEMA ESCURO / CLARO
  // ===========================================================================
  const body = document.body;
  const btnThemeToggle = document.getElementById("btn-theme-toggle");
  const themeIcon = document.getElementById("theme-icon");

  const savedTheme = localStorage.getItem("calcify_theme") || "dark";
  if (savedTheme === "light") {
    body.classList.remove("theme-dark");
    body.classList.add("theme-light");
    themeIcon.textContent = "🌙";
  } else {
    body.classList.add("theme-dark");
    body.classList.remove("theme-light");
    themeIcon.textContent = "☀️";
  }

  btnThemeToggle.addEventListener("click", () => {
    if (body.classList.contains("theme-light")) {
      body.classList.remove("theme-light");
      body.classList.add("theme-dark");
      themeIcon.textContent = "☀️";
      localStorage.setItem("calcify_theme", "dark");
    } else {
      body.classList.remove("theme-dark");
      body.classList.add("theme-light");
      themeIcon.textContent = "🌙";
      localStorage.setItem("calcify_theme", "light");
    }
  });

  // ===========================================================================
  // 2. NAVEGAÇÃO ENTRE ABAS
  // ===========================================================================
  const navTabs = document.querySelectorAll(".nav-tab");
  const tabPanels = document.querySelectorAll(".tab-panel");

  navTabs.forEach(tab => {
    tab.addEventListener("click", () => {
      const targetId = tab.dataset.tab;

      navTabs.forEach(t => {
        t.classList.remove("active");
        t.setAttribute("aria-selected", "false");
      });
      tabPanels.forEach(p => p.classList.remove("active"));

      tab.classList.add("active");
      tab.setAttribute("aria-selected", "true");

      const activePanel = document.getElementById(`tab-${targetId}`);
      if (activePanel) {
        activePanel.classList.add("active");
      }
    });
  });

  // ===========================================================================
  // 3. SISTEMA DE NOTIFICAÇÕES (TOAST)
  // ===========================================================================
  const toastContainer = document.getElementById("toast-container");

  function showToast(mensagem, tipo = "error") {
    const toast = document.createElement("div");
    toast.className = `toast toast-${tipo}`;
    toast.innerHTML = `<span>${tipo === "error" ? "⚠️" : "✨"}</span> <span>${mensagem}</span>`;

    toastContainer.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = "0";
      toast.style.transform = "translateX(100%)";
      toast.style.transition = "all 0.3s ease";
      setTimeout(() => toast.remove(), 300);
    }, 4000);
  }

  // ===========================================================================
  // 4. CALCULADORA CIENTÍFICA (VISOR E TECLADO)
  // ===========================================================================
  const displayValue = document.getElementById("display-value");
  const displayExpr = document.getElementById("display-expr");
  const btnDegRad = document.getElementById("btn-deg-rad");
  const historyList = document.getElementById("history-list");
  const historyBadge = document.getElementById("history-badge");
  const historyDrawer = document.getElementById("history-drawer");
  const btnHistoryToggle = document.getElementById("btn-history-toggle");
  const btnClearHistory = document.getElementById("btn-clear-history");
  const btnCloseHistory = document.getElementById("btn-close-history");

  // Estado da calculadora
  let currentValue = "0";
  let activeExpression = "";
  let firstOperand = null;
  let pendingOperator = null;
  let resetOnNextInput = false;
  let isAngleInDegrees = true;
  let history = JSON.parse(localStorage.getItem("calcify_history") || "[]");

  function updateDisplay() {
    displayValue.textContent = currentValue;
    displayExpr.textContent = activeExpression;
    btnDegRad.textContent = isAngleInDegrees ? "DEG" : "RAD";
    btnDegRad.title = isAngleInDegrees ? "Modo Graus ativo (Clique para alternar para Radianos)" : "Modo Radianos ativo (Clique para alternar para Graus)";
  }

  // Alternador Graus / Radianos
  btnDegRad.addEventListener("click", () => {
    isAngleInDegrees = !isAngleInDegrees;
    updateDisplay();
    showToast(`Modo alterado para ${isAngleInDegrees ? "Graus (DEG)" : "Radianos (RAD)"}`, "success");
  });

  // Histórico
  function renderHistory() {
    if (history.length === 0) {
      historyList.innerHTML = `<div class="history-empty">Nenhum cálculo recente.</div>`;
      historyBadge.style.display = "none";
      return;
    }

    historyBadge.style.display = "inline-block";
    historyBadge.textContent = history.length;

    historyList.innerHTML = "";
    history.slice().reverse().forEach(item => {
      const card = document.createElement("div");
      card.className = "history-item";
      card.innerHTML = `
        <div class="hist-expr">${item.expression}</div>
        <div class="hist-res">${item.result}</div>
      `;
      card.addEventListener("click", () => {
        currentValue = String(item.result);
        activeExpression = "";
        resetOnNextInput = true;
        updateDisplay();
        showToast(`Valor ${item.result} carregado no visor`, "success");
      });
      historyList.appendChild(card);
    });
  }

  function addHistoryItem(expression, result) {
    history.push({ expression, result });
    if (history.length > 40) history.shift();
    localStorage.setItem("calcify_history", JSON.stringify(history));
    renderHistory();
  }

  btnClearHistory.addEventListener("click", () => {
    history = [];
    localStorage.removeItem("calcify_history");
    renderHistory();
    showToast("Histórico limpo com sucesso", "success");
  });

  btnHistoryToggle.addEventListener("click", () => {
    historyDrawer.classList.toggle("closed");
  });

  btnCloseHistory.addEventListener("click", () => {
    historyDrawer.classList.add("closed");
  });

  // Iniciar drawer fechado no mobile ou aberto no desktop se houver itens
  if (window.innerWidth < 800) {
    historyDrawer.classList.add("closed");
  }
  renderHistory();

  // Chamadas assíncronas ao backend Flask
  async function executarOperacaoBackend(endpoint, payload) {
    try {
      const resp = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await resp.json();
      if (!data.success) {
        throw new Error(data.error || "Erro no cálculo");
      }
      return data;
    } catch (err) {
      showToast(err.message, "error");
      throw err;
    }
  }

  // Ações do Teclado da Calculadora
  async function handleKeyAction(action, val) {
    // 1. Números
    if (action === "num") {
      if (resetOnNextInput || currentValue === "0" || currentValue === "Erro") {
        currentValue = val;
        resetOnNextInput = false;
      } else {
        if (currentValue.length < 16) {
          currentValue += val;
        }
      }
      updateDisplay();
      return;
    }

    // 2. Decimal
    if (action === "decimal") {
      if (resetOnNextInput || currentValue === "Erro") {
        currentValue = "0.";
        resetOnNextInput = false;
      } else if (!currentValue.includes(".")) {
        currentValue += ".";
      }
      updateDisplay();
      return;
    }

    // 3. Limpar Tudo (AC)
    if (action === "clear") {
      currentValue = "0";
      activeExpression = "";
      firstOperand = null;
      pendingOperator = null;
      resetOnNextInput = false;
      updateDisplay();
      return;
    }

    // 4. Backspace (⌫)
    if (action === "backspace") {
      if (resetOnNextInput || currentValue === "Erro") {
        currentValue = "0";
        resetOnNextInput = false;
      } else if (currentValue.length > 1) {
        currentValue = currentValue.slice(0, -1);
      } else {
        currentValue = "0";
      }
      updateDisplay();
      return;
    }

    // 5. Inverter Sinal (±)
    if (action === "sign") {
      if (currentValue === "0" || currentValue === "Erro") return;
      if (currentValue.startsWith("-")) {
        currentValue = currentValue.substring(1);
      } else {
        currentValue = "-" + currentValue;
      }
      updateDisplay();
      return;
    }

    // 6. Constantes Pi e Euler
    if (action === "pi") {
      currentValue = String(Math.PI);
      resetOnNextInput = true;
      updateDisplay();
      return;
    }
    if (action === "euler") {
      currentValue = String(Math.E);
      resetOnNextInput = true;
      updateDisplay();
      return;
    }

    // 7. Funções Científicas Unárias (sin, cos, tan, ln, log, fact, sqrt)
    const unaryActions = ["sin", "cos", "tan", "ln", "log", "fact", "sqrt"];
    if (unaryActions.includes(action)) {
      const num = parseFloat(currentValue);
      if (isNaN(num)) return;

      let opBackend = "";
      let exprLabel = "";
      let payload = {};

      if (action === "sin") {
        opBackend = "seno";
        exprLabel = `sen(${num}${isAngleInDegrees ? "°" : " rad"})`;
        payload = { operacao: "seno", angulo: num, em_graus: isAngleInDegrees };
      } else if (action === "cos") {
        opBackend = "cosseno";
        exprLabel = `cos(${num}${isAngleInDegrees ? "°" : " rad"})`;
        payload = { operacao: "cosseno", angulo: num, em_graus: isAngleInDegrees };
      } else if (action === "tan") {
        opBackend = "tangente";
        exprLabel = `tan(${num}${isAngleInDegrees ? "°" : " rad"})`;
        payload = { operacao: "tangente", angulo: num, em_graus: isAngleInDegrees };
      } else if (action === "ln") {
        opBackend = "logaritmo_natural";
        exprLabel = `ln(${num})`;
        payload = { operacao: "logaritmo_natural", x: num };
      } else if (action === "log") {
        opBackend = "logaritmo_base10";
        exprLabel = `log₁₀(${num})`;
        payload = { operacao: "logaritmo_base10", x: num };
      } else if (action === "fact") {
        opBackend = "fatorial";
        exprLabel = `${num}!`;
        payload = { operacao: "fatorial", n: num };
      } else if (action === "sqrt") {
        opBackend = "raiz_quadrada";
        exprLabel = `√(${num})`;
        payload = { operacao: "raiz_quadrada", radicando: num };
      }

      try {
        const res = await executarOperacaoBackend("/api/calcular", payload);
        const calcRes = res.resultado;
        activeExpression = `${exprLabel} =`;
        currentValue = String(calcRes);
        resetOnNextInput = true;
        addHistoryItem(exprLabel + " =", calcRes);
        updateDisplay();
      } catch (err) {
        // Notificação já enviada pelo executarOperacaoBackend
      }
      return;
    }

    // 8. Funções Binárias com símbolos (+, -, *, /, power, root_n)
    if (action === "op" || action === "power" || action === "root_n") {
      const num = parseFloat(currentValue);
      if (isNaN(num)) return;

      let opSymbol = val;
      let internalOp = "";

      if (action === "power") {
        opSymbol = "^";
        internalOp = "potencia";
      } else if (action === "root_n") {
        opSymbol = " n-raiz ";
        internalOp = "raiz_enesima";
      } else {
        if (val === "+") internalOp = "adicionar";
        if (val === "-") internalOp = "subtrair";
        if (val === "*") internalOp = "multiplicar";
        if (val === "/") internalOp = "dividir";
      }

      // Se já houver operação pendente, calcula antes de encadear
      if (firstOperand !== null && pendingOperator !== null && !resetOnNextInput) {
        await executePendingCalculation();
      }

      firstOperand = parseFloat(currentValue);
      pendingOperator = { op: internalOp, symbol: opSymbol };
      activeExpression = `${firstOperand} ${opSymbol}`;
      resetOnNextInput = true;
      updateDisplay();
      return;
    }

    // 9. Porcentagem Rápida (%)
    if (action === "pct") {
      const curr = parseFloat(currentValue);
      if (isNaN(curr)) return;

      if (firstOperand !== null && (pendingOperator.op === "adicionar" || pendingOperator.op === "subtrair")) {
        // Porcentagem relativa ao primeiro termo
        const pctVal = (firstOperand * curr) / 100.0;
        currentValue = String(pctVal);
      } else {
        currentValue = String(curr / 100.0);
      }
      resetOnNextInput = true;
      updateDisplay();
      return;
    }

    // 10. Botão Igual (=)
    if (action === "equals") {
      if (pendingOperator !== null && firstOperand !== null) {
        await executePendingCalculation();
      }
    }
  }

  async function executePendingCalculation() {
    const secondOperand = parseFloat(currentValue);
    if (isNaN(secondOperand)) return;

    let payload = {};
    if (pendingOperator.op === "potencia") {
      payload = { operacao: "potencia", base: firstOperand, expoente: secondOperand };
    } else if (pendingOperator.op === "raiz_enesima") {
      payload = { operacao: "raiz_enesima", radicando: firstOperand, indice: secondOperand };
    } else {
      payload = { operacao: pendingOperator.op, a: firstOperand, b: secondOperand };
    }

    try {
      const res = await executarOperacaoBackend("/api/calcular", payload);
      const resultadoFinal = res.resultado;
      const fullExpr = `${firstOperand} ${pendingOperator.symbol} ${secondOperand} =`;

      activeExpression = fullExpr;
      currentValue = String(resultadoFinal);
      addHistoryItem(fullExpr, resultadoFinal);

      firstOperand = null;
      pendingOperator = null;
      resetOnNextInput = true;
      updateDisplay();
    } catch (err) {
      // Erro amigável
    }
  }

  // Event listener para todos os botões do teclado
  document.querySelectorAll(".keypad-grid .btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const action = btn.dataset.action;
      const val = btn.dataset.val;
      handleKeyAction(action, val);
    });
  });

  // Suporte a teclado físico na aba Calculadora
  window.addEventListener("keydown", (e) => {
    const activeTab = document.querySelector(".nav-tab.active").dataset.tab;
    if (activeTab !== "calculadora") return;

    // Evitar interceptação caso foco esteja em algum input
    if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") return;

    if (e.key >= "0" && e.key <= "9") {
      handleKeyAction("num", e.key);
    } else if (e.key === "." || e.key === ",") {
      handleKeyAction("decimal", ".");
    } else if (e.key === "+") {
      handleKeyAction("op", "+");
    } else if (e.key === "-") {
      handleKeyAction("op", "-");
    } else if (e.key === "*") {
      handleKeyAction("op", "*");
    } else if (e.key === "/") {
      e.preventDefault();
      handleKeyAction("op", "/");
    } else if (e.key === "Enter" || e.key === "=") {
      e.preventDefault();
      handleKeyAction("equals");
    } else if (e.key === "Backspace") {
      handleKeyAction("backspace");
    } else if (e.key === "Escape") {
      handleKeyAction("clear");
    } else if (e.key === "%") {
      handleKeyAction("pct");
    }
  });


  // ===========================================================================
  // 5. EQUAÇÕES (1º E 2º GRAU)
  // ===========================================================================
  const formEq1 = document.getElementById("form-eq1");
  const eq1Result = document.getElementById("eq1-result");
  const eq1Solution = document.getElementById("eq1-solution");
  const eq1Steps = document.getElementById("eq1-steps");

  formEq1.addEventListener("submit", async (e) => {
    e.preventDefault();
    const a = parseFloat(document.getElementById("eq1-a").value);
    const b = parseFloat(document.getElementById("eq1-b").value);

    try {
      const res = await executarOperacaoBackend("/api/equacao/primeiro-grau", { a, b });
      const dados = res.dados;
      eq1Result.style.display = "block";
      if (dados.solucao !== null) {
        eq1Solution.textContent = `x = ${dados.solucao}`;
      } else {
        eq1Solution.textContent = dados.tipo === "infinitas" ? "Infinitas Soluções" : "Sem Solução Real";
      }
      eq1Steps.textContent = dados.explicacao;
      showToast("Equação de 1º grau resolvida com sucesso!", "success");
    } catch (err) {}
  });

  const formEq2 = document.getElementById("form-eq2");
  const eq2Result = document.getElementById("eq2-result");
  const eq2Solution = document.getElementById("eq2-solution");
  const eq2Steps = document.getElementById("eq2-steps");

  formEq2.addEventListener("submit", async (e) => {
    e.preventDefault();
    const a = parseFloat(document.getElementById("eq2-a").value);
    const b = parseFloat(document.getElementById("eq2-b").value);
    const c = parseFloat(document.getElementById("eq2-c").value);

    try {
      const res = await executarOperacaoBackend("/api/equacao/segundo-grau", { a, b, c });
      const dados = res.dados;
      eq2Result.style.display = "block";

      if (dados.tipo === "duas_reais") {
        eq2Solution.textContent = `x₁ = ${dados.x1}  |  x₂ = ${dados.x2}`;
      } else if (dados.tipo === "raiz_unica") {
        eq2Solution.textContent = `x = ${dados.x} (raiz dupla)`;
      } else if (dados.tipo === "sem_raizes_reais") {
        eq2Solution.textContent = "Não possui raízes reais (Δ < 0)";
      } else {
        eq2Solution.textContent = `x = ${dados.solucao}`;
      }
      eq2Steps.textContent = dados.explicacao;
      showToast("Equação de 2º grau resolvida com sucesso!", "success");
    } catch (err) {}
  });


  // ===========================================================================
  // 6. ESTATÍSTICA
  // ===========================================================================
  const formStat = document.getElementById("form-estatistica");
  const statInput = document.getElementById("stat-input");
  const statResults = document.getElementById("stat-results-container");
  const btnStatSample = document.getElementById("btn-stat-sample");
  const btnStatClear = document.getElementById("btn-stat-clear");

  btnStatSample.addEventListener("click", () => {
    statInput.value = "15, 28, 42.5, 9, 33, 42.5, 100, 7.8";
  });

  btnStatClear.addEventListener("click", () => {
    statInput.value = "";
    statResults.style.display = "none";
  });

  formStat.addEventListener("submit", async (e) => {
    e.preventDefault();
    const texto = statInput.value.trim();
    if (!texto) return;

    try {
      const res = await executarOperacaoBackend("/api/estatistica", { valores: texto });
      const est = res.estatisticas;
      document.getElementById("stat-media").textContent = Number(est.media.toFixed(4));
      document.getElementById("stat-mediana").textContent = est.mediana;
      document.getElementById("stat-maior").textContent = est.maior;
      document.getElementById("stat-menor").textContent = est.menor;
      document.getElementById("stat-qtd").textContent = est.quantidade;

      statResults.style.display = "grid";
      showToast("Dados estatísticos calculados!", "success");
    } catch (err) {}
  });


  // ===========================================================================
  // 7. CONVERSÕES DE UNIDADES (INTERATIVAS EM TEMPO REAL)
  // ===========================================================================
  const convCelsius = document.getElementById("conv-celsius");
  const convFahrenheit = document.getElementById("conv-fahrenheit");

  convCelsius.addEventListener("input", async () => {
    const val = parseFloat(convCelsius.value);
    if (isNaN(val)) { convFahrenheit.value = ""; return; }
    try {
      const res = await executarOperacaoBackend("/api/conversao", { tipo: "celsius_fahrenheit", valor: val });
      convFahrenheit.value = Number(res.resultado.toFixed(2));
    } catch (e) {}
  });

  convFahrenheit.addEventListener("input", async () => {
    const val = parseFloat(convFahrenheit.value);
    if (isNaN(val)) { convCelsius.value = ""; return; }
    try {
      const res = await executarOperacaoBackend("/api/conversao", { tipo: "fahrenheit_celsius", valor: val });
      convCelsius.value = Number(res.resultado.toFixed(2));
    } catch (e) {}
  });

  const convKm = document.getElementById("conv-km");
  const convM = document.getElementById("conv-m");

  convKm.addEventListener("input", async () => {
    const val = parseFloat(convKm.value);
    if (isNaN(val)) { convM.value = ""; return; }
    try {
      const res = await executarOperacaoBackend("/api/conversao", { tipo: "km_m", valor: val });
      convM.value = res.resultado;
    } catch (e) {}
  });

  convM.addEventListener("input", async () => {
    const val = parseFloat(convM.value);
    if (isNaN(val)) { convKm.value = ""; return; }
    try {
      const res = await executarOperacaoBackend("/api/conversao", { tipo: "m_km", valor: val });
      convKm.value = res.resultado;
    } catch (e) {}
  });

  const convHoras = document.getElementById("conv-horas");
  const convMinutos = document.getElementById("conv-minutos");

  convHoras.addEventListener("input", async () => {
    const val = parseFloat(convHoras.value);
    if (isNaN(val)) { convMinutos.value = ""; return; }
    try {
      const res = await executarOperacaoBackend("/api/conversao", { tipo: "horas_minutos", valor: val });
      convMinutos.value = res.resultado;
    } catch (e) {}
  });

  convMinutos.addEventListener("input", async () => {
    const val = parseFloat(convMinutos.value);
    if (isNaN(val)) { convHoras.value = ""; return; }
    try {
      const res = await executarOperacaoBackend("/api/conversao", { tipo: "minutos_horas", valor: val });
      convMinutos.value = res.resultado;
    } catch (e) {}
  });


  // ===========================================================================
  // 8. PORCENTAGEM (CARDS DEDICADOS)
  // ===========================================================================
  document.getElementById("form-pct-valor").addEventListener("submit", async (e) => {
    e.preventDefault();
    const p = parseFloat(document.getElementById("pct-p").value);
    const val = parseFloat(document.getElementById("pct-val").value);
    try {
      const res = await executarOperacaoBackend("/api/calcular", { operacao: "porcentagem_de_valor", percentual: p, valor: val });
      document.getElementById("res-pct-valor").style.display = "flex";
      document.getElementById("val-pct-valor").textContent = res.resultado;
      showToast(`${p}% de ${val} = ${res.resultado}`, "success");
    } catch (e) {}
  });

  document.getElementById("form-pct-aumento").addEventListener("submit", async (e) => {
    e.preventDefault();
    const val = parseFloat(document.getElementById("aum-val").value);
    const p = parseFloat(document.getElementById("aum-p").value);
    try {
      const res = await executarOperacaoBackend("/api/calcular", { operacao: "aumento_percentual", valor: val, percentual: p });
      document.getElementById("res-pct-aumento").style.display = "flex";
      document.getElementById("val-pct-aumento").textContent = res.resultado;
      showToast(`Valor final com aumento: ${res.resultado}`, "success");
    } catch (e) {}
  });

  document.getElementById("form-pct-desconto").addEventListener("submit", async (e) => {
    e.preventDefault();
    const val = parseFloat(document.getElementById("desc-val").value);
    const p = parseFloat(document.getElementById("desc-p").value);
    try {
      const res = await executarOperacaoBackend("/api/calcular", { operacao: "desconto_percentual", valor: val, percentual: p });
      document.getElementById("res-pct-desconto").style.display = "flex";
      document.getElementById("val-pct-desconto").textContent = res.resultado;
      showToast(`Valor final com desconto: ${res.resultado}`, "success");
    } catch (e) {}
  });

});
