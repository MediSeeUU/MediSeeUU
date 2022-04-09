// external imports
import React, { Component } from 'react'
import Col from 'react-bootstrap/Col'
import Row from 'react-bootstrap/Row'
import Container from 'react-bootstrap/Container'
import 'bootstrap/dist/css/bootstrap.min.css'
import ApexCharts from 'apexcharts'

// internal imports
import VisualizationForm from '../forms/VisualizationForm'
import BarChart from '../visualization_types/bar_chart'
import LineGraph from '../visualization_types/line_graph'
import DonutChart from '../visualization_types/donut_chart'
import BoxPlot from '../visualization_types/box_plot'
import GenerateBarSeries from '../data_interfaces/BarInterface'
import GenerateLineSeries from '../data_interfaces/LineInterface'
import GeneratePieSeries from '../data_interfaces/PieInterface'
import HandleSVGExport from './exports/HandleSVGExport'
import HandlePNGExport from './exports/HandlePNGExport'
import GetUniqueCategories from '../utils/GetUniqueCategories'

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
    let uniqueCategories = GetUniqueCategories(this.props.data)

    // generating the initial series data
    let series = GenerateBarSeries(
      {
        chartSpecificOptions: {
          xAxis: 'DecisionYear',
          yAxis: 'Rapporteur',
          categoriesSelected: [],
        },
      },
      uniqueCategories,
      this.props.data
    )

    // state initialization
    this.state = {
      chart_type: 'bar',
      chartSpecificOptions: {
        xAxis: 'DecisionYear',
      },
      legend_on: false,
      labels_on: false,
      data: this.props.data,
      series: series,
      allUniqueCategories: uniqueCategories,
      changeName: '',
    }

    // event handlers
    this.handleChange = this.handleChange.bind(this)
    this.handlePNGExport = this.handlePNGExport.bind(this)
    this.handleSVGExport = this.handleSVGExport.bind(this)
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
    ApexCharts.getChartByID(this.props.id).updateOptions({
      dataLabels: { enabled: event.labels_on },
      legend: { show: event.legend_on },
    })
  }

  // handles the png export
  handlePNGExport(event) {
    HandlePNGExport(this.props.id, ApexCharts)
  }

  // handles the svg export
  handleSVGExport(event) {
    HandleSVGExport(this.props.id, ApexCharts)
  }





  // creating a chart based on the chosen chart type
  createChart(chart_type) {
    const legend_on = this.state.legend_on
    const labels_on = this.state.labels_on
    const id = this.props.id

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
            id={id}
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
          <LineGraph
            key={`${this.state.changeName} 
			              ${this.state.chartSpecificOptions[this.state.changeName]}`}
            legend={legend_on}
            labels={labels_on}
            id={id}
            series={this.state.series}
            categories={
              this.state.allUniqueCategories[
                this.state.chartSpecificOptions.xAxis
              ]
            }
            options={this.state.chartSpecificOptions}
          />
        )

      case 'donut':
        return (
          <DonutChart
            key={`${this.state.changeName}
                    ${this.state.chartSpecificOptions[this.state.changeName]}`}
            legend={legend_on}
            labels={labels_on}
            id={id}
            series={this.state.series}
            categories={this.state.chartSpecificOptions.categoriesSelected}
            options={this.state.chartSpecificOptions}
          />
        )

      case 'boxPlot':
        return <BoxPlot legend={legend_on} labels={labels_on} id={id} />

      default:
        return (
          <BarChart legend={legend_on} labels={labels_on} id={id} />
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
      case 'bar':
        return GenerateBarSeries(
          options,
          this.state.allUniqueCategories,
          this.state.data
        )

      case 'line':
        return GenerateLineSeries(
          options,
          this.state.allUniqueCategories,
          this.state.data
        )

      case 'donut':
        return GeneratePieSeries(
          options,
          this.state.allUniqueCategories,
          this.state.data
        )

      default:
        return GenerateBarSeries(options)
    }
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
      <div className="table-holder">
        <Container>
          <Row>
            <Col className="visualization-panel">
              <VisualizationForm
                uniqueCategories={this.state.allUniqueCategories}
                onFormChange={this.handleChange}
              />
            </Col>
            <Col sm={8}>
              <Row className="visualization-title">
                <input
                  type="text"
                  id={'graphName' + this.props.id}
                  className="graph-name"
                  placeholder="Enter a graph name"
                  autoComplete="off"
                />
              </Row>
              <Row>{this.createChart(this.state.chart_type)}</Row>
              <Row>
                <button
                  className="table-buttons button-export"
                  onClick={this.handlePNGExport}
                >
                  <i className="bx bx-save filter-Icon"></i>Export as PNG
                </button>
                <button
                  className="table-buttons button-export"
                  onClick={this.handleSVGExport}
                >
                  <i className="bx bx-save filter-Icon"></i>Export as SVG
                </button>
                <button
                  className="table-buttons button-remove"
                  onClick={this.props.onRemoval}
                  value={this.props.id}
                >
                  <i className="bx bx-trash"></i> Remove visualization
                </button>
              </Row>
            </Col>
          </Row>
        </Container>
      </div>
    )
  }
}

export default SingleVisualization
