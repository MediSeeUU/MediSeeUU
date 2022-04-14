import React, { Component } from 'react'
import Chart from 'react-apexcharts'

// line graph component
class LineChart extends Component {
  constructor(props) {
    super(props)

    this.state = {
      hasError: false,
      options: {
        chart: {
          id: String(this.props.id),
          type: 'line',
          toolbar: { show: false },
        },
        xaxis: {
          categories: this.props.categories,
          labels: {
            hideOverlappingLabels: true,
          },
          overwriteCategories: this.props.categories,
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

  // render a line graph
  render() {
    if(this.state.hasError) {
      return <div>An error has occurred when drawing the chart</div>
    } else {
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
}

export default LineChart
