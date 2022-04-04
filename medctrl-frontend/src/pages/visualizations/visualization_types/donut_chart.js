import React, { Component } from 'react'
import Chart from 'react-apexcharts'

// pie chart component
class DonutChart extends Component {
  constructor(props) {
    super(props)

    this.state = {
      options: {
        chart: {
          id: String(this.props.number),
          type: "pie",
          toolbar: {show: "false"}
        },
        dataLabels: {
          enabled: this.props.labels,
        },
        legend: {
          show: this.props.legend,
        },
      },
      series: this.props.series,
      labels: this.props.categories,
    }
  }

  // renders a pie chart
  render() {
    return (
      <div className="donut">
        <Chart
          options={this.state.options}
          series={this.state.series}
          type="donut"
        />
      </div>
    )
  }
}

export default DonutChart
