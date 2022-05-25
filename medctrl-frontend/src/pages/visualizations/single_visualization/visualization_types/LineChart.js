import React from 'react'
import Chart from 'react-apexcharts'

// line graph component
function LineChart(props) {
  let settings = {
    options: {
      chart: {
        id: String(props.id),
        type: 'line',
        toolbar: { show: false },
        events: {
          dataPointSelection: (event, chartContext, config) => {
            let euNumbers =
              config.w.config.series[config.seriesIndex].euNumbers[
                config.dataPointIndex
              ]
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
          text: props.options.yAxis,
        },
      },
      dataLabels: {
        enabled: props.labels,
      },
      legend: {
        show: props.legend,
      },
      noData: {
        test: `You can select the categories to be displayed.
           Note that creating the graph may take some time`,
      },
      theme: {
        palette: 'palette3',
      },
      tooltip: {
        intersect: true,
        shared: false,
      },
      markers: {
        size: 6,
      },
    },
    series: props.series,
  }

  // RENDERER:

  // render a line graph
  return (
    <Chart
      options={settings.options}
      series={settings.series}
      type="line"
      height={700}
    />
  )
}

export default LineChart
