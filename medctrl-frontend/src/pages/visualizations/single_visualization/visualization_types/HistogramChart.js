// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

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
        fontFamily: 'Poppins, sans-serif',
        foreColor: 'var(--text-primary)',
        events: {
          dataPointSelection: (event, chartContext, config) => {
            let eu_pnumbers =
              props.series[config.seriesIndex].eu_pnumbers[config.dataPointIndex]
            props.onDataClick(eu_pnumbers)
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
          style: {
            fontWeight: '300',
            fontSize: 'small',
            color: 'var(--text-primary)',
          },
        },
      },
      yaxis: {
        title: {
          text: 'Number',
          style: {
            fontWeight: '300',
            fontSize: 'small',
            color: 'var(--text-primary)',
          },
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
