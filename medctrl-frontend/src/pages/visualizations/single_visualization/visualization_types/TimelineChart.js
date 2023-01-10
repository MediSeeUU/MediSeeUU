// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'
import Chart from 'react-apexcharts'
import * as Colors from './Colors'

// timeline chart component
function TimelineChart(props) {
  let settings = {
    options: {
      chart: {
        id: String(props.id),
        type: 'timeline',
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
      colors: Colors.timeline_colors,
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
      plotOptions: { timeline: { expandOnClick: false } },

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

  // renders a timeline
  return (
    <Chart options={settings.options} series={settings.series} type="timeline" />
  )
}

export default TimelineChart
