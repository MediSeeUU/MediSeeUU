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
              let eu_numbers =
                config.w.config.series[config.seriesIndex].eu_numbers[
                  config.dataPointIndex
                ]
              this.props.onDataClick(eu_numbers)
            },
          },
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
          />
        </div>
      )
    } catch {
      return <div>An error occurred when drawing the chart</div>
    }
  }
}

export default LineChart
