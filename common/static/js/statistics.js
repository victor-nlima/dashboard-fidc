// ===========================================================================================
// ======================     js para as estatisticas     ===================================
// ===========================================================================================

let fluxoCaixaChart = echarts.init(document.getElementById('fluxo_caixa'), 'dark',
{renderer: 'canvas', useDirtyRect: false});

let current_box = document.getElementById('current_box').textContent
let cumulative_expected_flow = document.getElementById('cumulative_expected_flow').textContent

current_box = JSON.parse(current_box)

cumulative_expected_flow =  JSON.parse(cumulative_expected_flow)


console.log('teste',cumulative_expected_flow)

let fluxoCaixaOption;

fluxoCaixaOption = {
color: ['#c39b56', '#d1540a'],
backgroundColor: '#002e40',
title: {
    text: '',
    subtext: 'R$ mil'
},
tooltip: {
    trigger: 'axis',
    axisPointer: {
        type: 'shadow'
    },
    formatter: function (params) {
        // "params" é um array com as informações de cada série na categoria
        let categoryName = params[0].name;
        let sum = params.reduce(function (acc, cur) {
            return acc + cur.value;
        }, 0);
        let sumFormatted = sum.toLocaleString('pt-BR', {
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        });

        return (
            categoryName +
            '<br/>' + 'Total: R$' + sumFormatted + 'k'
        );
    }
},
legend: {
    data: ['Caixa Atual', 'Fluxo Esperado Acumulado']
},
grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
},
xAxis: {
    type: 'category',
    splitLine: {show: false},
    data: ['D+0', 'D+1', 'D+2', 'D+3', 'D+4', 'D+5', 'D+6', 'D+7']
},
yAxis: {
    type: 'value'
},
series: [
    {
        name: 'Caixa Atual',
        type: 'bar',
        stack: 'Total', // Identificador para empilhar
        label: {
            show: true,
            position: 'inside',
            formatter: function (params) {
                const valor = params.value; // Valor numérico
                if (valor === 0) {
                    // Se for zero, não exibe nada
                    return '';
                }

                // Caso contrário, formata o número
                return valor.toLocaleString('pt-BR', {
                    minimumFractionDigits: 0,
                    maximumFractionDigits: 0
                });
            }
        },
        data: current_box
    },
    {
        name: 'Fluxo Esperado Acumulado',
        type: 'bar',
        stack: 'Total', // Mesmo identificador para empilhar
        label: {
            show: true,
            position: 'inside',
            formatter: function (params) {
                const valor = params.value; // Valor numérico
                if (valor === 0) {
                    // Se for zero, não exibe nada
                    return '';
                }

                // Caso contrário, formata o número
                return valor.toLocaleString('pt-BR', {
                    minimumFractionDigits: 0,
                    maximumFractionDigits: 0
                });
            }
        },
        data: cumulative_expected_flow
    }
]
};


// Display the chart using the configuration items and data just specified.
fluxoCaixaChart.setOption(fluxoCaixaOption);
window.addEventListener('DOMContentLoaded', function () {
    fluxoCaixaChart();
});
