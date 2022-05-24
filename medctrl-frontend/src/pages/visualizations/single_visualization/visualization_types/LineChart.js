import React, { Component } from 'react'
import Chart from 'react-apexcharts'

// line graph component
class LineChart extends Component {
  constructor(props) {
    super(props)

    this.state = {
      options: {
        chart: {
          id: String(this.props.id),
          type: 'line',
          toolbar: { show: false },
          events: {
            dataPointSelection: (event, chartContext, config) => {
              let euNumbers =
                config.w.config.series[config.seriesIndex].euNumbers[
                  config.dataPointIndex
                ]
              this.props.onDataClick(euNumbers)
            },
          },
        },
        xaxis: {
          categories: this.props.categories,
          labels: {
            rotateAlways: true,
            trim: true,
          },
          tickPlacement: 'on',
          title: {
            text: this.props.options.xAxis,
          },
        },
        yaxis: {
          title: {
            text: this.props.options.yAxis,
          },
        },
        dataLabels: {
          enabled: this.props.labels,
        },
        legend: {
          show: this.props.legend,
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
      series: this.props.series,
    }
  }

  // RENDERER:

  // render a line graph
  render() {
    try {
      return (
        <div className="mixed-chart">
          <Chart
            options={this.state.options}
            series={this.state.series}
            type="line"
            height={700}
          />
        </div>
      )
    } catch {
      return <div>An error occurred when drawing the chart</div>
    }
  }
}

export default LineChart
