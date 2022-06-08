// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import React, { Component } from 'react'
import Chart from 'react-apexcharts'

// bar chart component
class BarChart extends Component {
  constructor(props) {
    super(props)

    // initializing the state with data passed from the form
    this.state = {
      options: {
        chart: {
          id: String(this.props.id),
          type: 'bar',
          stacked: this.props.options.stacked,
          stackType: this.props.options.stackType ? '100%' : 'normal',
          toolbar: { tools: { download: false } },
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
        plotOptions: {
          bar: {
            horizontal: this.props.options.horizontal,
            distributed: false,
          },
        },
        xaxis: {
          categories: this.props.categories,
          labels: {
            hideOverLappingLabels: false,
            rotateAlways: true,
            trim: true,
          },
          title: {
            text: this.props.options.horizontal
              ? this.props.options.yAxis
              : this.props.options.xAxis,
          },
        },
        yaxis: {
          title: {
            text: this.props.options.horizontal
              ? this.props.options.xAxis
              : this.props.options.yAxis,
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
        theme: {
          palette: 'palette3',
        },
      },
      series: this.props.series,
    }
  }

  // RENDERER:

  // renders the bar chart with the given options
  render() {
    // example code for adding a scroll bar to an axis
    //const dynamicWidth = this.state.series.length * 100;
    //const chartWidth = dynamicWidth < window.innerWidth ? '100%' : dynamicWidth;
    try {
      return (
        <div className="chart">
          <Chart
            options={this.state.options}
            series={this.state.series}
            type="bar"
            height={700}
            //width={chartWidth}
          />
        </div>
      )
    } catch {
      return <div>An error occurred when drawing the chart</div>
    }
  }
}

export default BarChart
