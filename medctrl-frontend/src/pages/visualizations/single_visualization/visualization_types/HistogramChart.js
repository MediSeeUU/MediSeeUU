import React, { Component } from 'react'
import Chart from 'react-apexcharts'

// histogram chart component
class HistogramChart extends Component {
  constructor(props) {
    super(props)

    this.state = {
      options: {
        chart: {
          id: String(this.props.id),
          type: 'bar',
          toolbar: { show: false },
          events: {
            dataPointSelection: (event, chartContext, config) => {
              let euNumbers =
                config.w.config.series[config.seriesIndex].euNumbers[
                  config.dataPointIndex
                ]
              this.props.onDataClick(euNumbers)
            },
          },
        },
        xaxis: {
          categories: this.props.categories,
          labels: {
            rotateAlways: true,
            trim: true,
          },
          tickPlacement: 'on',
          title: {
            text: this.props.options.xAxis,
          },
        },
        yaxis: {
          title: {
            text: 'number',
          },
        },
        dataLabels: {
          enabled: this.props.labels,
        },
        legend: {
          show: this.props.legend,
        },
        noData: {
          text: `You can select the categories to be displayed.
            Note that creating the graph may take some time`,
        },
        euNumbers: this.props.series.euNumbers,
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
            height={700}
          />
        </div>
      )
    } catch {
      return <div>An error occurred when drawing the chart</div>
    }
  }
}

export default HistogramChart
