import React from 'react'
import Chart from 'react-apexcharts'

// histogram chart component
function HistogramChart(props) {
  let settings = {
    options: {
      chart: {
        id: String(props.id),
        type: 'bar',
        toolbar: { show: false },
        events: {
          dataPointSelection: (event, chartContext, config) => {
            let euNumbers =
              props.series[config.seriesIndex].euNumbers[config.dataPointIndex]
            props.onDataClick(euNumbers)
          },
        },
      },
      xaxis: {
        categories: props.categories,
        labels: {
          rotateAlways: true,
          trim: true,
        },
        tickPlacement: 'on',
        title: {
          text: props.options.xAxis,
        },
      },
      yaxis: {
        title: {
          text: 'number',
        },
      },
      dataLabels: {
        enabled: props.labels,
      },
      legend: {
        show: props.legend,
      },
      noData: {
        text: `You can select the categories to be displayed.
            Note that creating the graph may take some time`,
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
    series: props.series,
  }

  // RENDERER:

  // renders a histogram chart
  return (
    <Chart
      options={settings.options}
      series={settings.series}
      type="bar"
      height={700}
    />
  )
}

export default HistogramChart
