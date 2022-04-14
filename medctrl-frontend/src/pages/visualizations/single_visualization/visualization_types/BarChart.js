import React, { Component } from 'react'
import Chart from 'react-apexcharts'

// bar chart component
class BarChart extends Component {
  constructor(props) {
    super(props)

    let stacktype
    if (this.props.options.stackType) {
      stacktype = '100%' // relative stacking
    } else {
      stacktype = 'normal' // absolute stacking
    }

    // initializing the state with data passed from the form
    this.state = {
      hasError: false,
      options: {
        chart: {
          id: String(this.props.id),
          type: 'bar',
          stacked: this.props.options.stacked,
          stackType: stacktype,
          toolbar: { show: false },
        },
        plotOptions: {
          bar: {
            horizontal: this.props.options.horizontal,
            distributed: false,
          },
        },
        xaxis: {
          categories: this.props.categories,
          labels: {
            hideOverlappingLabels: true,
          },
        },
        dataLabels: {
          enabled: this.props.labels,
        },
        legend: {
          show: this.props.legend,
        },
        noData: {
          text: 'pick your preferred options to create a visualization',
        },
      },
      series: this.props.series,
    }
  }

  // GENERAL FUNCTIONS:

  // error handler for when something in the chart generation goes wrong
  static getDerivedStateFromError(error, errorInfo) {
    return { hasError: true }
  }

  // RENDERER:

  // renders the bar chart with the given options
  render() {
    if (this.state.hasError) {
      return <div>An error has occurred when drawing the chart</div>
    } else {
      return (
        <div className="mixed-chart">
          <Chart
            options={this.state.options}
            series={this.state.series}
            type="bar"
          />
        </div>
      )
    }
  }
}

export default BarChart
