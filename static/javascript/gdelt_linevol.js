Chart.defaults.scale.gridLines.display = false;
new Chart(document.getElementById("line-chart"), {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{ 
          data: val1,
          label: "Volume",
          borderColor: "#3e95cd",
          fill: false,
          pointRadius: 0
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: 'Coverage Volume Intensity'
      },
      tooltips:{
        enabled:true,
        mode:'nearest',
        intersect:false

      },
      scales: {
        yAxes: [{
          scaleLabel: {
            display: true,
            labelString: 'Monitored Articles'
          }
        }]
      }   
    }
  });