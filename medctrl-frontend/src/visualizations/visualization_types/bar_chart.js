import React, { Component } from "react";
import Chart from "react-apexcharts";

// bar chart component
class BarChart extends Component {
  constructor(props) {
    super(props);
    console.log(this.props.categories);
    let seriess = this.toSeriesFormat(this.props.series);

    this.state = {
      options: {
        chart: {
          id: String(this.props.number),
          type: "bar",
          stacked: true,
          stackType: '100%'
        },
        plotOptions: {
          bar: {
            horizontal: true,
            distributed: false
          }
        },
        xaxis: {
          categories: this.props.categories["DecisionYear"] //[1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999]
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
    console.log(dict);
    let series = [];
    for (let key in dict) {
      console.log(key);
      series.push({name: key, data: dict[key]})
    }

    //console.log(series);
    return series;
  }



  // renders the bar chart with the given options
  render() {
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