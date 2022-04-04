import React, { Component } from 'react'
import Col from 'react-bootstrap/Col'
import Row from 'react-bootstrap/Row'
import Container from 'react-bootstrap/Container'
import 'bootstrap/dist/css/bootstrap.min.css'
import { changeDpiDataUrl } from 'changedpi'
import Exports from 'apexcharts/src/modules/Exports'
import ApexCharts from 'apexcharts'

import VisualizationForm from './visualization_form'
import BarChart from './visualization_types/bar_chart'
import LineGraph from './visualization_types/line_graph'
import DonutChart from './visualization_types/donut_chart'
import BoxPlot from './visualization_types/box_plot'

import GenerateBarSeries from './data_interfaces/bar_interface'

// renders the components for a single visualization
class SingleVisualization extends Component {
  constructor(props) {
    // receives its id and a copy of the data
    super(props)

    /*
      Gets the categories of all the variables.
      Right now the filter for the visualizations has not been implemented,
      so this should not change.
      Keep in mind that the categories for all variables are sorted,
      this is important for interfacing with the ApexCharts library!
    */
    let uniqueCategories = this.getUniqueCategories(this.props.data)

    // generating the initial series data
    let series = GenerateBarSeries({
      chartSpecificOptions: {
        xAxis: "DecisionYear",
        yAxis: "Rapporteur",
        categoriesSelected: ["United Kingdom"]
      }
    }, uniqueCategories, this.props.data)

    // state initialization
    this.state = {
      chart_type: 'bar',
      chartSpecificOptions: { 
        xAxis: 'DecisionYear'
      },
      legend_on: false,
      labels_on: false,
      data: this.props.data,
      series: series,
      allUniqueCategories: uniqueCategories,
      changeName: ''
    }

    // event handlers
    this.handleChange = this.handleChange.bind(this)
    this.handleExport = this.handleExport.bind(this)
  }

  // event handler for the form data
  handleChange(event) {
    const series = this.generateSeries(event.chart_type, event)

    this.setState({
      chart_type: event.chart_type,
      chartSpecificOptions: event.chartSpecificOptions,
      legend_on: event.legend_on,
      labels_on: event.labels_on,
      series: series,
      changeName: event.chartSpecificOptionsName,
    })

    /*
      Actually updating the parameters of the chart
      we may want to do this purely using the states,
      currently not sure if that would be more efficient
    */
    ApexCharts.getChartByID(this.props.number).updateOptions({
      dataLabels: { enabled: event.labels_on },
      legend: { show: event.legend_on },
    })
  }

  /*
	  Event handler for exporting the visualization to svg and png.
		Does not export the actual data.
		Currently does both the svg and the png export at once,
		seperate buttons should be made!
	*/
  handleExport(event) {
    /* 
		  Get the visualization in the base64 format,
			we scale it for a better resolution.
		*/
    ApexCharts.exec(String(this.props.number), 'dataURI', { scale: 3.5 }).then(
      ({ imgURI }) => {
        // changes the dpi of the visualization to 300
        const dataURI300 = changeDpiDataUrl(imgURI, 300)
        let exp = new Exports(
          ApexCharts.getChartByID(String(this.props.number))
        )

        /*
          Does not currently export it using the title of the visualization,
          as the title is not currently set as an option for the user to enter.
        */
        exp.triggerDownload(
          dataURI300,
          exp.w.config.chart.toolbar.export.png.filename,
          '.png'
        )
        exp.exportToSVG(ApexCharts.getChartByID(String(this.props.number)))
      }
    )
  }

  // creating a chart based on the chosen chart type
  createChart(chart_type) {
    const legend_on = this.state.legend_on
    const labels_on = this.state.labels_on
    const number = this.props.number

    switch (chart_type) {
      case 'bar':
        return (
          <BarChart
           // Perhaps just using an increment function may be better,
           // like in visualization page
            key={`${this.state.changeName} 
			              ${this.state.chartSpecificOptions[this.state.changeName]}`}
            legend={legend_on}
            labels={labels_on}
            number={number}
            series={this.state.series}
            categories={
              this.state.allUniqueCategories[
                this.state.chartSpecificOptions.xAxis
              ]
            }
            options={this.state.chartSpecificOptions}
          />
        )

      case 'line':
        return (
          <LineGraph legend={legend_on} labels={labels_on} number={number} />
        )

      case 'donut':
        return (
          <DonutChart legend={legend_on} labels={labels_on} number={number} />
        )

      case 'boxPlot':
        return <BoxPlot legend={legend_on} labels={labels_on} number={number} />

      default:
        return (
          <BarChart legend={legend_on} labels={labels_on} number={number} />
        )
    }
  }

  /*
    Returns series data depending on the chart type,
    as each chart type expects data in a certain way.
    For example, a pie chart only expect one variable,
    whereas a bar chart expect two.
  */
  generateSeries(chartType, options) {
    switch (chartType) {
      case "bar":
        return GenerateBarSeries(
          options,
          this.state.allUniqueCategories,
          this.state.data
        )

      default:
        return GenerateBarSeries(options)
    }
  }

  // takes the (JSON) data and gets the categories for each variable
  getUniqueCategories(data) {
    let dict = {}

    // element is a single 'database entry'
    data.forEach((element) => {
      for (let attribute in element) {
        let val = element[attribute]
        if (dict[attribute] === undefined) {
          dict[attribute] = [val]
        } else {
          if (!dict[attribute].includes(val)) {
            dict[attribute].push(val)
          }
        }
      }
    })

    // sorting the array
    for (let categories in dict) {
      dict[categories] = dict[categories].sort(function(a, b) {
        return String(a).localeCompare(String(b), "en", {
          numeric: true,
          sensitivity: "base"
        })
      })
    }
    
    return dict
  }

  /*
	  Renders a single visualization,
		based on the layout from the prototype:
		divides the visualization in a left part for the form,
		a right-lower part for the visualization and 
		a right-upper part for the filters.
	*/
  render() {
    return (
      <div>
        <Container>
          <Row>
            <Col
              sm={4}
              style={{
                backgroundColor: 'grey',
                borderRadius: '15px',
                borderRight: '2px solid black',
              }}
            >
              <VisualizationForm
                uniqueCategories={this.state.allUniqueCategories}
                onFormChange={this.handleChange}
              />
            </Col>
            <Col sm={8}>
              <Row>hello</Row>
              <Row>{this.createChart(this.state.chart_type)}</Row>
            </Col>
          </Row>
          <Row>
            <button onClick={this.handleExport}>Print to svg</button>
          </Row>
        </Container>
      </div>
    )
  }
}

export default SingleVisualization
