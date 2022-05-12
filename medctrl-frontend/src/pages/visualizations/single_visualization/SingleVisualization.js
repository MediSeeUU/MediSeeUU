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

// renders the components for a single visualization
class SingleVisualization extends Component {
  constructor(props) {
    // receives its id and a copy of the data
    super(props)

    /*
      Gets the categories of all the variables.
      Right now the filter for the visualizations has not been implemented,
      so this should not change.
      Keep in mind that the categories for all variables will be sorted,
      this is important for interfacing with the ApexCharts library!
    */

    this.settings = this.props.settings

    // event handlers
    this.handleChange = this.handleChange.bind(this)
    this.handlePNGExport = this.handlePNGExport.bind(this)
    this.handleSVGExport = this.handleSVGExport.bind(this)
    this.handleRemoval = this.handleRemoval.bind(this)
  }

  // EVENT HANDLERS:

  // event handler for the form data
  handleChange(event) {
    this.settings.chart_type = event.chart_type
    this.settings.chartSpecificOptions = event.chartSpecificOptions
    this.settings.legend_on = event.legend_on
    this.settings.labels_on = event.labels_on
    this.settings.changeName = event.chartSpecificOptionsName
    var currentSetting =
      this.settings.chartSpecificOptions.yAxis ??
      this.settings.chartSpecificOptions.chosenVariable
    this.settings.chartSpecificOptions.selectAllCategories =
      this.settings.chartSpecificOptions.categoriesSelected?.length ===
      this.settings.uniqueCategories[currentSetting].length

    this.settings.series = generateSeries(
      this.settings.chart_type,
      this.settings
    )
    this.props.onFormChangeFunc(this.settings)

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
    this.props.onRemoval(this.props.settings.id, event)
  }

  // GENERAL FUNCTIONS:

  // creating a chart based on the chosen chart type
  createChart(chart_type) {
    const key = `${this.settings.changeName} 
			              ${this.settings.chartSpecificOptions[this.settings.changeName]}`
    const legend_on = this.settings.legend_on
    const labels_on = this.settings.labels_on
    const id = this.props.id
    const series = this.settings.series

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
              this.settings.uniqueCategories[
                this.settings.chartSpecificOptions.xAxis
              ]
            }
            options={this.settings.chartSpecificOptions}
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
              this.settings.uniqueCategories[
                this.settings.chartSpecificOptions.xAxis
              ]
            }
            options={this.settings.chartSpecificOptions}
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
            categories={this.settings.chartSpecificOptions.categoriesSelected}
            options={this.settings.chartSpecificOptions}
          />
        )

      default:
        throw Error(
          'visualization settings incorrect settings: {' + this.settings + '}'
        )
    }
  }

  handleNameChange(event) {
    this.settings.chartName = event.target.value
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
      <div className="med-content-container visual-container">
        <Container>
          <Row>
            <Col className="visualization-panel">
              <VisualizationForm
                uniqueCategories={this.settings.uniqueCategories}
                onFormChange={this.handleChange}
                settings={this.settings}
              />
            </Col>
            <Col sm={8}>
              <Row className="visualization-title">
                <input
                  tour='step-vis-main'
                  type="text"
                  id={'graphName' + this.props.id}
                  className="graph-name med-text-input"
                  placeholder="Enter a graph name"
                  autoComplete="off"
                  value={this.settings.chartName}
                  onChange={this.handleNameChange.bind(this)}
                />
              </Row>
              <Row>{this.createChart(this.settings.chart_type)}</Row>
              <Row>
                <button
                  className="med-primary-solid med-bx-button button-export"
                  onClick={this.handlePNGExport}
                >
                  <i className="bx bx-save filter-Icon"></i>Export as PNG
                </button>
                <button
                  className="med-primary-solid med-bx-button button-export"
                  onClick={this.handleSVGExport}
                >
                  <i className="bx bx-save filter-Icon"></i>Export as SVG
                </button>
                <button
                  className="med-primary-solid med-bx-button button-remove"
                  onClick={this.handleRemoval}
                  value={this.props.id}
                >
                  <i className="bx bx-trash"></i>
                </button>
              </Row>
            </Col>
          </Row>
        </Container>
      </div>
    )
  }
}

/*
Returns series data depending on the chart type,
as each chart type expects data in a certain way.
For example, a pie chart only expect one variable,
whereas a bar chart expect two.
*/
export function generateSeries(chartType, options) {
  switch (chartType) {
    case 'bar':
      return GenerateBarSeries(options, options.uniqueCategories, options.data)

    case 'line':
      return GenerateLineSeries(options, options.uniqueCategories, options.data)

    case 'pie':
      return GeneratePieSeries(options, options.data)

    default:
      throw Error(
        'visualization settings incorrect settings: {' + this.settings + '}'
      )
  }
}

export default SingleVisualization
