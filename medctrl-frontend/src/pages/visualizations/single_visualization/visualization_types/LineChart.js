// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
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
        fontFamily: 'Poppins, sans-serif',
        foreColor: 'var(--text-primary)',
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
          style: {
            fontWeight: '300',
            fontSize: 'small',
            color: 'var(--text-primary)',
          },
        },
      },
      yaxis: {
        title: {
          text: props.options.yAxis,
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
