import React, { Component } from 'react'
import Chart from 'react-apexcharts'

// pie chart component
class DonutChart extends Component {
  constructor(props) {
    super(props)

    console.log(props)
    this.state = {
      options: {
        chart: {
          id: String(this.props.number),
          type: 'pie',
          toolbar: { show: false },
        },
        dataLabels: {
          enabled: this.props.labels,
        },
        legend: {
          show: this.props.legend,
        },
        labels: this.props.categories,
        noData: {
          text: "pick your preferred options to create a visualization"
        }
      },
      series: this.props.series,
    }
  }

  // renders a pie chart
  render() {
    return (
      <div className="donut">
        <Chart
          options={this.state.options}
          series={this.state.series}
          type="pie"
        />
      </div>
    )
  }
}

export default DonutChart
