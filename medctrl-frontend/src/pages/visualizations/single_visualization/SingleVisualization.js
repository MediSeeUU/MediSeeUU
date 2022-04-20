// external imports
import React, { Component } from 'react'
import Col from 'react-bootstrap/Col'
import Row from 'react-bootstrap/Row'
import Container from 'react-bootstrap/Container'
import 'bootstrap/dist/css/bootstrap.min.css'
import ApexCharts from 'apexcharts'

// internal imports
import VisualizationForm from './forms/VisualizationForm'
import BarChart from './visualization_types/BarChart'
import LineChart from './visualization_types/LineChart'
import PieChart from './visualization_types/PieChart'
import GenerateBarSeries from './data_interfaces/BarInterface'
import GenerateLineSeries from './data_interfaces/LineInterface'
import GeneratePieSeries from './data_interfaces/PieInterface'
import HandleSVGExport from './exports/HandleSVGExport'
import HandlePNGExport from './exports/HandlePNGExport'
import GetUniqueCategories from './utils/GetUniqueCategories'
import ContentContainer from '../../../shared/container/ContentContainer'

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
      uniqueCategories: uniqueCategories,
      changeName: '',
    }

    // event handlers
    this.handleChange = this.handleChange.bind(this)
    this.handlePNGExport = this.handlePNGExport.bind(this)
    this.handleSVGExport = this.handleSVGExport.bind(this)
    this.handleRemoval = this.handleRemoval.bind(this)
  }

  // EVENT HANDLERS:

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
    ApexCharts.getChartByID(String(this.props.id)).updateOptions({
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

  // handles the removal of this visualization
  handleRemoval(event) {
    this.props.onRemoval(this.props.id, event)
  }

  // GENERAL FUNCTIONS:

  // creating a chart based on the chosen chart type
  createChart(chart_type) {
    const key = `${this.state.changeName} 
			              ${this.state.chartSpecificOptions[this.state.changeName]}`
    const legend_on = this.state.legend_on
    const labels_on = this.state.labels_on
    const id = this.props.id
    const series = this.state.series

    switch (chart_type) {
      case 'bar':
        return (
          <BarChart
            key={key}
            legend={legend_on}
            labels={labels_on}
            id={id}
            series={series}
            categories={
              this.state.uniqueCategories[this.state.chartSpecificOptions.xAxis]
            }
            options={this.state.chartSpecificOptions}
          />
        )

      case 'line':
        return (
          <LineChart
            key={key}
            legend={legend_on}
            labels={labels_on}
            id={id}
            series={series}
            categories={
              this.state.uniqueCategories[this.state.chartSpecificOptions.xAxis]
            }
            options={this.state.chartSpecificOptions}
          />
        )

      case 'pie':
        return (
          <PieChart
            key={key}
            legend={legend_on}
            labels={labels_on}
            id={id}
            series={series}
            categories={this.state.chartSpecificOptions.categoriesSelected}
            options={this.state.chartSpecificOptions}
          />
        )

      default:
        return (
          <BarChart
            key={key}
            legend={legend_on}
            labels={labels_on}
            id={id}
            series={series}
            categories={
              this.state.uniqueCategories[this.state.chartSpecificOptions.xAxis]
            }
            options={this.state.chartSpecificOptions}
          />
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
          this.state.uniqueCategories,
          this.state.data
        )

      case 'line':
        return GenerateLineSeries(
          options,
          this.state.uniqueCategories,
          this.state.data
        )

      case 'pie':
        return GeneratePieSeries(
          options,
          this.state.uniqueCategories,
          this.state.data
        )

      default:
        return GenerateBarSeries(options)
    }
  }

  // RENDERER:

  /*
	  Renders a single visualization,
		based on the layout from the prototype:
		divides the visualization in a left part for the form,
		a right-lower part for the visualization and 
		a right-upper part for the filters.
	*/
  render() {
    return (
      <ContentContainer className='visual-container'>
        <Container>
          <Row>
            <Col className="visualization-panel">
              <VisualizationForm
                uniqueCategories={this.state.uniqueCategories}
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
                  onClick={this.handleRemoval}
                  value={this.props.id}
                >
                  <i className="bx bx-trash"></i>
                </button>
              </Row>
            </Col>
          </Row>
        </Container>
      </ContentContainer>
    )
  }
}

export default SingleVisualization
