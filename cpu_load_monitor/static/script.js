const socket = io();
let selectedChart = 'cpu';
let chartRefs = {};
const colors = {
  cpu: 'rgba(0, 200, 255, 0.9)',
  cpu0: 'rgba(0, 255, 128, 0.9)',
  cpu1: 'rgba(255, 165, 0, 0.9)'
};

const createChart = (ctx, label, color, showAxisTitles = false) => {
  return new Chart(ctx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [{
        label: label,
        data: [],
        borderColor: color,
        backgroundColor: color.replace('0.9', '0.2'),
        tension: 0.3,
        fill: true
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: false,
      scales: {
        x: {  display: true,
              title: {
                display: showAxisTitles,
                text: 'Time',
                color: '#cccccc'
              },
              ticks: {
                display: false
              },
              grid: {
                display: false
              },
              lineWidth: 2.5
            },
        y: {  display: true,
              beginAtZero: true,
              suggestedMax: 100,
              title: {
                display: showAxisTitles,
                text: 'Usage (%)',
                color: '#cccccc'
              },
            }, 
            lineWidth: 2.5
        },
      plugins: {
        legend: { display: false }
      }
    }
  });
};

const updateChart = (chart, value) => {
  const time = new Date().toLocaleTimeString();
  chart.data.labels.push(time);
  chart.data.datasets[0].data.push(value);
  if (chart.data.labels.length > 50) {
    chart.data.labels.shift();
    chart.data.datasets[0].data.shift();
  }
  chart.update();
};

function selectChart(type) {
  selectedChart = type;
  document.getElementById('mainChartTitle').innerText = `${type.toUpperCase()} Usage`;
  updateMainChart();
}

function updateMainChart() {
  const ctx = document.getElementById('mainChartCanvas').getContext('2d');
  if (chartRefs.main) chartRefs.main.destroy();
  chartRefs.main = createChart(ctx, selectedChart.toUpperCase(), colors[selectedChart], true);
}

socket.on('system_data', data => {
  if (!chartRefs.miniCpu) {
    chartRefs.miniCpu = createChart(document.getElementById('miniCpu').getContext('2d'), 'CPU', colors.cpu);
    chartRefs.miniCpu0 = createChart(document.getElementById('miniCpu0').getContext('2d'), 'CPU_0', colors.cpu0);
    chartRefs.miniCpu1 = createChart(document.getElementById('miniCpu1').getContext('2d'), 'CPU_1', colors.cpu1);
    updateMainChart();
  }
  
  updateChart(chartRefs.miniCpu, data.cpu);
  updateChart(chartRefs.miniCpu0, data.cpu0);
  updateChart(chartRefs.miniCpu1, data.cpu1);
  
  if (chartRefs.main && selectedChart) {
    updateChart(chartRefs.main, data[selectedChart]);
  }
  
  document.getElementById('currentTime').innerText = 'Time: ' + new Date().toLocaleTimeString();
  document.getElementById('paramA').innerText = 'FW version: ' + "--";
  document.getElementById('paramB').innerText = 'UI version: ' + "--";
});

document.getElementById('themeSwitch').addEventListener('change', () => {
  document.body.classList.toggle('light');
  document.body.classList.toggle('dark');
});
