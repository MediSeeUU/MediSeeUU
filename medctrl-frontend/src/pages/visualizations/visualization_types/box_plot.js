import React, { Component } from 'react'
import Chart from 'react-apexcharts'

// box plot component
class BoxPlot extends Component {
  constructor(props) {
    super(props)
    this.state = {
      series: [
        {
          name: 'box',
          type: 'boxPlot',
          data: [
            {
              x: new Date('2017-01-01').getTime(),
              y: [54, 66, 69, 75, 88],
            },
            {
              x: new Date('2018-01-01').getTime(),
              y: [43, 65, 69, 76, 81],
            },
            {
              x: new Date('2019-01-01').getTime(),
              y: [31, 39, 45, 51, 59],
            },
            {
              x: new Date('2020-01-01').getTime(),
              y: [39, 46, 55, 65, 71],
            },
            {
              x: new Date('2021-01-01').getTime(),
              y: [29, 31, 35, 39, 44],
            },
          ],
        },
        {
          name: 'outliers',
          type: 'scatter',
          data: [
            {
              x: new Date('2017-01-01').getTime(),
              y: 32,
            },
            {
              x: new Date('2018-01-01').getTime(),
              y: 25,
            },
            {
              x: new Date('2019-01-01').getTime(),
              y: 64,
            },
            {
              x: new Date('2020-01-01').getTime(),
              y: 27,
            },
            {
              x: new Date('2020-01-01').getTime(),
              y: 78,
            },
            {
              x: new Date('2021-01-01').getTime(),
              y: 15,
            },
          ],
        },
      ],
      options: {
        chart: {
          type: 'boxPlot',
          height: 350,
          id: String(this.props.number),
        },
        colors: ['#008FFB', '#FEB019'],
        title: {
          text: 'BoxPlot - Scatter Chart',
          align: 'left',
        },
        xaxis: {
          type: 'datetime',
          tooltip: {
            formatter: function (val) {
              return new Date(val).getFullYear()
            },
          },
        },
        tooltip: {
          shared: false,
          intersect: true,
        },
        dataLabels: {
          enabled: this.props.labels,
        },
        legend: {
          show: this.props.legend,
        },
      },
    }
  }

  // renders a box plot
  render() {
    return (
      <div className="mixed-chart">
        <Chart
          options={this.state.options}
          series={this.state.series}
          type="boxPlot"
        />
      </div>
    )
  }
}

export default BoxPlot
