// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

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
        fontFamily: 'Poppins, sans-serif',
        foreColor: 'var(--text-primary)',
        events: {
          dataPointSelection: (event, chartContext, config) => {
            let euNumbers = props.series.euNumbers[config.dataPointIndex]
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
      states: {
        active: {
          allowMultipleDataPointsSelection: false,
          filter: {
            type: 'none',
          },
        },
      },
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
