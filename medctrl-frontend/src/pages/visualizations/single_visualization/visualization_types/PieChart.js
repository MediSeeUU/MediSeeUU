import React, { Component } from 'react'
import Chart from 'react-apexcharts'

// pie chart component
class PieChart extends Component {
  constructor(props) {
    super(props)

    this.state = {
      options: {
        chart: {
          id: String(this.props.id),
          type: 'pie',
          toolbar: { tools: { download: false } },
        },
        dataLabels: {
          enabled: this.props.labels,
        },
        legend: {
          show: this.props.legend,
        },
        labels: this.props.categories,
        noData: {
          text: 'select the categories to be displayed',
        },
        plotOptions: { pie: { expandOnClick: false } },
      },
      series: this.props.series,
    }
  }

  // RENDERER:

  // renders a pie chart
  render() {
    try {
      return (
        <div className="donut">
          <Chart
            options={this.state.options}
            series={this.state.series}
            type="pie"
          />
        </div>
      )
    } catch {
      return <div>An error occurred when drawing the chart</div>
    }
  }
}

export default PieChart
