import React from 'react'
import Chart from 'react-apexcharts'

// pie chart component
function PieChart(props) {
  let settings = {
    options: {
      chart: {
        id: String(props.id),
        type: 'pie',
        toolbar: { show: false },
        events: {
          dataPointSelection: (event, chartContext, config) => {
            let euNumbers = config.w.config.euNumbers[config.dataPointIndex]
            props.onDataClick(euNumbers)
          },
        },
      },
      dataLabels: {
        enabled: props.labels,
      },
      legend: {
        show: props.legend,
      },
      labels: props.categories,
      noData: {
        text: `You can select the categories to be displayed.
           Note that creating the graph may take some time`,
      },
      plotOptions: { pie: { expandOnClick: false } },
      theme: {
        palette: 'palette3',
      },
      euNumbers: props.series.euNumbers,
    },
    series: props.series.data,
  }
  // RENDERER:

  // renders a pie chart
  return (
    <Chart options={settings.options} series={settings.series} type="pie" />
  )
}

export default PieChart
