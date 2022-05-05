import React, { Component } from 'react'
import Chart from 'react-apexcharts'

// pie chart component
class DonutChart extends Component {
  constructor(props) {
    super(props)

    this.state = {
      options: {
        chart: {
          id: String(this.props.id),
          type: 'pie',
          toolbar: { show: false },
          events: {
            dataPointSelection: (event, chartContext, config) => {
              let eu_numbers = config.w.config.metaData[config.dataPointIndex]
              this.props.onDataClick(eu_numbers)
            }
          },
        },
        dataLabels: {
          enabled: this.props.labels,
        },
        legend: {
          show: this.props.legend,
        },
        labels: this.props.categories,
        noData: {
          text: 'pick your preferred options to create a visualization',
        },
        plotOptions: { pie: { expandOnClick: false } },
        metaData: this.props.series.eu_numbers
      },
      series: this.props.series.data,
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

export default DonutChart
