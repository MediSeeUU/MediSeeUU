import React, { Component } from 'react'
import Chart from 'react-apexcharts'

// line graph component
class LineGraph extends Component {
  constructor(props) {
    super(props)

    this.state = {
      options: {
        chart: {
          id: String(this.props.number),
          type: "line",
          toolbar: {show: false}
        },
        xaxis: {
          categories: this.props.categories,
          labels: {
            hideOverLappingLabels: true
          }
        },
        dataLabels: {
          enabled: this.props.labels,
        },
        legend: {
          show: this.props.legend,
        },
        noData: {
          test: "pick your preferred options to create a visualization"
        }
      },
      series: this.props.series
    }
  }

  // render a line graph
  render() {
    return (
      <div className="mixed-chart">
        <Chart
          options={this.state.options}
          series={this.state.series}
          type="line"
        />
      </div>
    )
  }
}

export default LineGraph
