import React, { Component } from "react";
import Chart from "react-apexcharts";

// bar chart component
class BarChart extends Component {
  constructor(props) {
    super(props);

    this.state = {
      options: {
        chart: {
          id: String(this.props.number)
        },
        xaxis: {
          categories: [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999]
        },
        dataLabels: {
          enabled: this.props.labels
        },
        legend: {
          show: this.props.legend
        }
      },
      series: [
        {
          name: "series-1",
          data: [30, 40, 45, 50, 49, 60, 70, 91]
        }
      ]
    };
  }

  // renders the bar chart with the given options
  render() {
    return (
          <div className="mixed-chart">
            <Chart
              options={this.state.options}
              series={this.state.series}
              type= "bar"
            />
          </div>
    );
  }
}

export default BarChart