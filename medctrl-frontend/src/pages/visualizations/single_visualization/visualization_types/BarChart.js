// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'
import Chart from 'react-apexcharts'

// bar chart component
function BarChart(props) {
  // initializing the state with data passed from the form
  let settings = {
    options: {
      chart: {
        id: String(props.id),
        type: 'bar',
        toolbar: { show: false },
        stacked: props.options.stacked,
        stackType: props.options.stackType ? '100%' : 'normal',
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
      plotOptions: {
        bar: {
          horizontal: props.options.horizontal,
          distributed: false,
        },
      },
      xaxis: {
        categories: props.categories,
        labels: {
          hideOverLappingLabels: false,
          rotateAlways: true,
          trim: true,
        },
        // Explicitly left as 'between' rather than 'on',
        // as 'on' seems to not display some datapoints at the edges of the x axis
        tickPlacement: 'between',
        title: {
          text: props.options.horizontal
            ? props.options.yAxis
            : props.options.xAxis,
          style: {
            fontWeight: '300',
            fontSize: 'small',
            color: 'var(--text-primary)',
          },
        },
      },
      yaxis: {
        title: {
          text: props.options.horizontal
            ? props.options.xAxis
            : props.options.yAxis,
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
    series: props.series,
  }

  // RENDERER:

  // renders the bar chart with the given options

  // example code for adding a scroll bar to an axis
  //const dynamicWidth = settings.series.length * 100;
  //const chartWidth = dynamicWidth < window.innerWidth ? '100%' : dynamicWidth;
  return (
    <div className="med-vis-chart">
      <Chart
        options={settings.options}
        series={settings.series}
        type="bar"
        height={700}
        //width={chartWidth}
      />
    </div>
  )
}

export default BarChart
