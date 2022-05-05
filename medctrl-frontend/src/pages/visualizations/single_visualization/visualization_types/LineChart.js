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
          toolbar: { tools: { download: false } },
        },
        xaxis: {
          categories: this.props.categories,
          labels: {
            hideOverlappingLabels: true,
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
          text: 'select the categories to be displayed',
        },
        theme: {
          palette: 'palette3',
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
