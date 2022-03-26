import React, { Component } from "react";
import Chart from "react-apexcharts";

// bar chart component
class BarChart extends Component {
  constructor(props) {
    super(props);
    //console.log(this.props.categories);
    let seriess = this.toSeriesFormat(this.props.series);

    this.state = {
      options: {
        chart: {
          id: String(this.props.number),
          type: "bar",
          stacked: this.props.options.stacked,
          stackType: this.props.options.stackType
        },
        plotOptions: {
          bar: {
            horizontal: this.props.options.horizontal,
            distributed: false
          }
        },
        xaxis: {
          categories: this.props.categories
        },
        dataLabels: {
          enabled: this.props.labels
        },
        legend: {
          show: this.props.legend
        }
      },
      series: seriess
    };
  }

  toSeriesFormat(dict) {
    //console.log(dict);
    let series = [];
    for (let key in dict) {
     // console.log(key);
      series.push({name: key, data: dict[key]})
    }

    //console.log(series);
    return series;
  }



  // renders the bar chart with the given options
  render() {
    console.log(this.state.series);
    return (
          <div className="mixed-chart">
            <Chart
              options={this.state.options}
              series={this.state.series}
              type= "bar"
              //width={1000}
            />
          </div>
    );
  }
}

export default BarChart