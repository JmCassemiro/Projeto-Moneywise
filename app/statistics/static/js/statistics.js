const layoutTemplate = {
  font: { color: "#E6E6E6", family: "Josefin Sans, sans-serif" },
  paper_bgcolor: "#1F1F23",
  plot_bgcolor: "#1F1F23",
  xaxis: {
    color: "#999999",
    gridcolor: "#323232",
    tickfont: { family: "Josefin Sans, sans-serif" },
  },
  yaxis: {
    color: "#999999",
    gridcolor: "#323232",
    tickfont: { family: "Josefin Sans, sans-serif" },
  },
  legend: {
    font: { color: "#E6E6E6", family: "Josefin Sans, sans-serif" },
    bgcolor: "#1F1F23",
    bordercolor: "#323232",
  },
  margin: { l: 40, r: 40, t: 60, b: 40 },
};

// 🟡 Adiciona isso aqui no topo!
const coresPorCategoria = {
  Casa: "#F7B7B7",
  Viagem: "#B2D7F6",
  Entretenimento: "#F1D7A7",
  Estudos: "#B7D6B5",
  Saúde: "#F5D1D1",
  Mercado: "#D0E5D7",
};

document.addEventListener("DOMContentLoaded", function () {
  // === 1. Gráfico de pizza - Receitas por categoria ===
  const receitasLabels = receitasPorCategoria.map((item) => item[0]);
  const receitasValues = receitasPorCategoria.map((item) =>
    parseFloat(item[1])
  );
  const receitasColors = receitasLabels.map(
    (categoria) => coresPorCategoria[categoria] || "#CCCCCC"
  );

  Plotly.newPlot(
    "graficoReceitasCategoria",
    [
      {
        type: "pie",
        labels: receitasLabels,
        values: receitasValues,
        textinfo: "label+percent",
        hole: 0.4,
        marker: {
          colors: receitasColors,
        },
      },
    ],
    { ...layoutTemplate }
  );

  // === 2. Gráfico de pizza - Despesas por categoria ===
  const despesasLabels = despesasPorCategoria.map((item) => item[0]);
  const despesasValues = despesasPorCategoria.map((item) =>
    parseFloat(item[1])
  );
  const despesasColors = despesasLabels.map(
    (categoria) => coresPorCategoria[categoria] || "#CCCCCC"
  );

  Plotly.newPlot(
    "graficoDespesasCategoria",
    [
      {
        type: "pie",
        labels: despesasLabels,
        values: despesasValues,
        textinfo: "label+percent",
        hole: 0.4,
        marker: {
          colors: despesasColors,
        },
      },
    ],
    { ...layoutTemplate }
  );

  // === 3. Gráfico de linha - Evolução do saldo ===
  const datas = saldoEvolucao.map((item) => item[0]);
  const saldos = saldoEvolucao.map((item) => parseFloat(item[1]));

  Plotly.newPlot(
    "graficoEvolucaoSaldo",
    [
      {
        x: datas,
        y: saldos,
        type: "scatter",
        mode: "lines+markers",
        line: { shape: "linear", color: "#038FA7" },
        marker: { color: "#038FA7" },
      },
    ],
    {
      ...layoutTemplate,
      xaxis: { ...layoutTemplate.xaxis, title: "Data" },
      yaxis: { ...layoutTemplate.yaxis, title: "Saldo (R$)" },
    }
  );

  // === 4. Gráfico de barras - Comparativo receitas x despesas ===
  const meses = comparativoMensal.map((item) => item[0]);
  const receitasMes = comparativoMensal.map((item) => parseFloat(item[1]));
  const despesasMes = comparativoMensal.map((item) => parseFloat(item[2]));

  Plotly.newPlot(
    "graficoComparativo",
    [
      {
        x: meses,
        y: receitasMes,
        name: "Receitas",
        type: "bar",
        marker: {
          color: "#92CA7E",
          line: { color: "#92CA7E" },
        },
      },
      {
        x: meses,
        y: despesasMes,
        name: "Despesas",
        type: "bar",
        marker: {
          color: "#CA7E7E",
          line: { color: "#CA7E7E" },
        },
      },
    ],
    {
      ...layoutTemplate,
      barmode: "group",
      xaxis: { ...layoutTemplate.xaxis, title: "Mês" },
      yaxis: { ...layoutTemplate.yaxis, title: "Valor (R$)" },
    }
  );

  // === 4.1 Gráfico de linha - Receita, Despesa e Lucro ao longo do tempo ===
  const lucrosMes = receitasMes.map(
    (receita, index) => receita - despesasMes[index]
  );

  Plotly.newPlot(
    "graficoInvestimento",
    [
      {
        x: meses,
        y: receitasMes,
        name: "Receitas",
        type: "scatter",
        mode: "lines+markers",
        line: { shape: "spline", color: "#92CA7E", width: 3 },
      },
      {
        x: meses,
        y: despesasMes,
        name: "Despesas",
        type: "scatter",
        mode: "lines+markers",
        line: { shape: "spline", color: "#CA7E7E", width: 3 },
      },
      {
        x: meses,
        y: lucrosMes,
        name: "Saldo",
        type: "scatter",
        mode: "lines+markers",
        line: { shape: "spline", color: "#038FA7", width: 4, dash: "dashdot" },
      },
    ],
    {
      ...layoutTemplate,
      xaxis: { ...layoutTemplate.xaxis, title: "Mês" },
      yaxis: { ...layoutTemplate.yaxis, title: "Valor (R$)" },
    }
  );

  // === 5. Gráfico de barra horizontal - Top 5 maiores despesas ===
  const top5Ordenado = top5Despesas
    .slice()
    .sort((a, b) => parseFloat(b[1]) - parseFloat(a[1]))
    .reverse();

  const top5Labels = top5Ordenado.map((item) => item[0]);
  const top5Valores = top5Ordenado.map((item) => parseFloat(item[1]));

  Plotly.newPlot(
    "graficoTop5Despesas",
    [
      {
        y: top5Labels,
        x: top5Valores,
        type: "bar",
        orientation: "h",
        marker: { color: "#CA7E7E" },
      },
    ],
    {
      ...layoutTemplate,
      xaxis: { ...layoutTemplate.xaxis, title: "Valor (R$)" },
    }
  );
});
