//(function () {
const config = {
  type: "line",
  data: {
    labels: [],
    datasets: [
      // {
      //   label: "Random Dataset",
      //   backgroundColor: "rgb(255, 99, 132)",
      //   borderColor: "rgb(255, 99, 132)",
      //   data: [],
      //   fill: false,
      // },
    ],
  },
  options: {
    elements: {
      line: {
        tension: 0,
      },
    },
    responsive: true,
    title: {
      display: true,
      text: "Creating Real-Time Charts with Flask",
    },
    tooltips: {
      mode: "index",
      intersect: false,
    },
    hover: {
      mode: "nearest",
      intersect: true,
    },
    scales: {
      xAxes: [
        {
          display: true,
          scaleLabel: {
            display: true,
            labelString: "Time",
          },
        },
      ],
      yAxes: [
        {
          display: true,
          scaleLabel: {
            display: true,
            labelString: "Value",
          },
        },
      ],
    },
  },
};

const context = document.getElementById("canvas").getContext("2d");

const lineChart = new Chart(context, config);

const randColNum = function () {
  return Math.floor(Math.random() * 256);
};

let i = 0;
const onMessage = function (e) {
  const data = JSON.parse(e.data);
  if (config.data.datasets.length === 0) {
    data.forEach(function (el) {
      const color = `rgb(${randColNum()}, ${randColNum()}, ${randColNum()})`;
      config.data.datasets.push({
        label: el,
        backgroundColor: color,
        borderColor: color,
        data: [],
        fill: false,
      });
    });
  } else if (!Array.isArray(data)) {
    if (config.data.labels.length === 100) {
      config.data.labels.shift();
      config.data.datasets.forEach(function (el) {
        el.data.shift();
      });
    }
    config.data.labels.push(i);
    i++;
    //config.data.labels.push(data.time);
    //JSON.parse(data.values).forEach(function (value, ind) {
      config.data.datasets[0].data.push(parseFloat(data.value));
    //});
    console.log(data)
  }
  lineChart.update();
};

const startSource = function () {
  const start = new EventSource("/chart-data");
  start.onmessage = onMessage;
  return start;
};
let source = startSource();

document.getElementById("pause").addEventListener("click", function () {
  source.close();
  source = null;
  console.log("burh");
});
document.getElementById("continue").addEventListener("click", function () {
  if (!source) source = startSource();
});
//})();
