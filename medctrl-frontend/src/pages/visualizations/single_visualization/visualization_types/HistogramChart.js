import React, { Component } from 'react'
import Chart from 'react-apexcharts'

// histogram chart component
class HistogramChart extends Component {
  constructor(props) {
    super(props)

    console.log(this.props.series)
    this.state = {
      options: {
        chart: {
          id: String(this.props.id),
          type: 'bar',
          toolbar: { tools: { download: false } },
        },
        xaxis: {
          categories: this.props.categories,
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
      },
      series: this.props.series,
    }
  }

  // RENDERER:

  // renders a histogram chart
  render() {
    try {
      return (
        <div>
          <Chart
            options={this.state.options}
            series={this.state.series}
            type="bar"
          />
        </div>
      )
    } catch {
      return <div>An error occurred when drawing the chart</div>
    }
  }
}

export default HistogramChart
