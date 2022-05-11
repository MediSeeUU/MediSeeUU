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
          toolbar: { tools: { download: false } },
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
            text: 'amount',
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
        eu_numbers: this.props.series.eu_numbers,
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
