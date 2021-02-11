Chart.defaults.scale.gridLines.display = false;
new Chart(document.getElementById("bar-chart"), {
    type: 'bar',
    data: {
    labels: labels_1,
    datasets: [
        {
        label: "Total",
        borderColor: "rgb(0, 127, 255)",
        backgroundColor: "rgba(0, 127, 255, 0.3)",
        borderWidth: 1.5,
        data: data_1,
        }
    ]
    },
    options: {
    legend: { display: false },
    title: {
        display: true,
        text: 'HOURLY VISIT'
    }
    }
});

new Chart(document.getElementById("bar-chart1"), {
    type: 'bar',
    data: {
      labels: labels_2,
      datasets: [
        {
          label: "Score",
          backgroundColor: "rgba(13, 71, 161, 0.3)",
          borderColor:"rgba(13, 71, 161, 1)",
          borderWidth:1.5,
          data: data_2
        }
      ]
    },
    options: {
  
      legend: { display: false },
      title: {
        display: true,
        text: 'BUSINESS SCORE : TODAY'
      }
    }
});