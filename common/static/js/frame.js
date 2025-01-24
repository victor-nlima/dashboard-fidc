// ============================================================
// ============   js para o enquadramento   ===================
// ============================================================

let myChart = echarts.init(document.getElementById('main'), 'dark', {
  renderer: 'canvas',
  useDirtyRect: false
});

let common_debtor = document.getElementById('common_debtor').textContent
let common_debtor_transform = document.getElementById('common_debtor_transform').textContent
let special_debtor = document.getElementById('special_debtor').textContent
let special_debtor_transform = document.getElementById('special_debtor_transform').textContent

common_debtor = JSON.parse(common_debtor)
common_debtor_transform = JSON.parse(common_debtor_transform)
special_debtor = JSON.parse(special_debtor)
special_debtor_transform =  JSON.parse(special_debtor_transform)

let option;

option = {
  backgroundColor: '#002e40',
  title: {
    text: 'Descritivo',
    subtext: '% do patrimônio'
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow'
    },
    formatter: function (params) {
      let tar = params[1];
      let valorFormatado = (tar.value).toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      });
      return tar.name + '<br/>' + tar.seriesName + ' : ' + valorFormatado + '%';
    }
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    splitLine: { show: false },
    data: ['Top 1', 'Grupo 2', 'Grupo 3', 'Grupo 4', 'Grupo 5', 'Top 5', 'Grupo 6', 'Grupo 7', 'Grupo 8', 'Grupo 9', 'Grupo 10', 'Top 10']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      name: 'Placeholder',
      type: 'bar',
      stack: 'Total',
      itemStyle: {
        borderColor: 'transparent',
        color: 'transparent'
      },
      emphasis: {
        itemStyle: {
          borderColor: 'transparent',
          color: 'transparent'
        }
      },
      data: common_debtor
    },
    {
      name: 'Percentual Acumulado',
      type: 'bar',
      stack: 'Total',
      label: {
        show: true,
        position: 'inside'
      },
      itemStyle: {
        color: '#e3e3e3'
      },

      data: common_debtor_transform
    }
  ]
};

myChart.setOption(option);
window.addEventListener('resize', function () {
  myChart.resize();
});


let myChart2 = echarts.init(document.getElementById('main2'), 'dark', {
  renderer: 'canvas',
  useDirtyRect: false
});

let option2;

option2 = {
  backgroundColor: '#002e40',
  title: {
    text: 'Descritivo',
    subtext: '% do patrimônio'
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow'
    },
    formatter: function (params) {
      let tar = params[1];
      let valorFormatado = (tar.value).toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      });
      return tar.name + '<br/>' + tar.seriesName + ' : ' + valorFormatado + '%';
    }
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    splitLine: { show: false },
    data: ['Top 1', 'Grupo 2', 'Grupo 3', 'Grupo 4', 'Grupo 5', 'Top 5']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      name: 'Placeholder',
      type: 'bar',
      stack: 'Total',
      itemStyle: {
        borderColor: 'transparent',
        color: 'transparent'
      },
      emphasis: {
        itemStyle: {
          borderColor: 'transparent',
          color: 'transparent'
        }
      },
      data: special_debtor
    },
    {
      name: 'Percentual Acumulado',
      type: 'bar',
      stack: 'Total',
      label: {
        show: true,
        position: 'inside'
      },
      itemStyle: {
        color: '#e3e3e3'
      },
      data: special_debtor_transform
    }
  ]
};

// Display the chart using the configuration items and data just specified.
myChart2.setOption(option2);
window.addEventListener('resize', function () {
  myChart2.resize();
});

