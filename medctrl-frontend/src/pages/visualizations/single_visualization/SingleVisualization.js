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
import HistogramChart from './visualization_types/HistogramChart'
import GenerateBarSeries from './data_interfaces/BarInterface'
import GenerateLineSeries from './data_interfaces/LineInterface'
import GeneratePieSeries from './data_interfaces/PieInterface'
import GenerateHistogramSeries from './data_interfaces/HistogramInterface'
import HandleSVGExport from './exports/HandleSVGExport'
import HandlePNGExport from './exports/HandlePNGExport'
import sortCategoryData from './utils/SortCategoryData'

// renders the components for a single visualization
class SingleVisualization extends Component {
  constructor(props) {
    // Receives its id, the selected data, the settings and
    // two event handlers for removing or changing the visualization.
    super(props)

    // initializing 'state' of the visualization
    this.settings = this.props.settings

    // event handlers
    this.handleChange = this.handleChange.bind(this)
    this.handlePNGExport = this.handlePNGExport.bind(this)
    this.handleSVGExport = this.handleSVGExport.bind(this)
    this.handleRemoval = this.handleRemoval.bind(this)
    this.handleNameChange = this.handleNameChange.bind(this)
  }

  // EVENT HANDLERS:

  // event handler for the form data
  handleChange(event) {
    this.settings.chartType = event.chartType
    this.settings.chartSpecificOptions = event.chartSpecificOptions
    this.settings.legendOn = event.legendOn
    this.settings.labelsOn = event.labelsOn
    this.settings.changeName = event.chartSpecificOptionsName

    this.settings.series = generateSeries(
      this.settings.chartType,
      this.settings
    )

    this.props.onFormChangeFunc(this.settings)
  }

  // handles the png export
  handlePNGExport(event) {
    const title = this.settings.title ?? this.renderTitlePlaceHolder()
    HandlePNGExport(this.props.id, title, ApexCharts)
  }

  // handles the svg export
  handleSVGExport(event) {
    const title = this.settings.title ?? this.renderTitlePlaceHolder()
    HandleSVGExport(this.props.id, title, ApexCharts)
  }

  // handles the removal of this visualization
  handleRemoval(event) {
    this.props.onRemoval(this.props.settings.id, event)
  }

  // handles changing the title of the visualization
  handleNameChange(event) {
    this.settings.title = event.target.value
    this.props.onFormChangeFunc(this.settings)
  }

  // GENERAL FUNCTIONS:

  // creating a chart based on the chosen chart type
  renderChart() {
    const newValue =
      this.settings.chartSpecificOptions[this.settings.changeName] ??
      this.settings[this.settings.changeName]
    const key = `${this.settings.changeName}${newValue}`
    const legendOn = this.settings.legendOn
    const labelsOn = this.settings.labelsOn
    const id = this.props.id
    const series = this.settings.series
    const categories = sortCategoryData(
      this.settings.chartSpecificOptions.categoriesSelectedX
    )
    const options = this.settings.chartSpecificOptions
    const onDataClick = this.props.onDataClick

    switch (this.settings.chartType) {
      case 'bar':
        return (
          <BarChart
            key={key}
            legend={legendOn}
            labels={labelsOn}
            id={id}
            series={series}
            categories={categories}
            options={options}
            onDataClick={onDataClick}
          />
        )

      case 'line':
        return (
          <LineChart
            key={key}
            legend={legendOn}
            labels={labelsOn}
            id={id}
            series={series}
            categories={categories}
            options={options}
            onDataClick={onDataClick}
          />
        )

      case 'pie':
        return (
          <PieChart
            key={key}
            legend={legendOn}
            labels={labelsOn}
            id={id}
            series={series}
            categories={categories}
            options={options}
            onDataClick={onDataClick}
          />
        )

      case 'histogram':
        return (
          <HistogramChart
            key={key}
            legend={legendOn}
            labels={labelsOn}
            id={id}
            series={series}
            categories={categories}
            options={options}
            onDataClick={onDataClick}
          />
        )

      default:
        throw Error(
          'visualization settings incorrect settings: {' + this.settings + '}'
        )
    }
  }

  // renders the placeholder for the title depending on the chart type
  renderTitlePlaceHolder() {
    const chartType = 'my ' + this.settings.chartType
    switch (this.settings.chartType) {
      case 'bar':
        return (
          chartType +
          ' - ' +
          this.settings.chartSpecificOptions.xAxis +
          ' vs ' +
          this.settings.chartSpecificOptions.yAxis
        )

      case 'line':
        return (
          chartType +
          ' - ' +
          this.settings.chartSpecificOptions.xAxis +
          ' vs ' +
          this.settings.chartSpecificOptions.yAxis
        )

      case 'pie':
        return chartType + ' - ' + this.settings.chartSpecificOptions.xAxis

      case 'histogram':
        return chartType + ' - ' + this.settings.chartSpecificOptions.xAxis

      default:
        throw Error(
          'visualization settings incorrect settings: {' + this.settings + '}'
        )
    }
  }

  // RENDERER:

  // Renders a single visualization,
  // based on the layout from the prototype:
  // divides the visualization in a left part for the form,
  // a right-lower part for the visualization and
  // a right-upper part for the filters.
  render() {
    return (
      <div className="med-content-container visual-container">
        <Container>
          <Row>
            <Col className="visualization-panel">
              <VisualizationForm
                uniqueCategories={this.settings.uniqueCategories}
                onChange={this.handleChange}
                settings={this.settings}
              />
            </Col>
            <Col sm={8}>
              <Row>
                <input
                  type="text"
                  id={'graphName' + this.props.id}
                  className="graph-name med-text-input"
                  placeholder={this.renderTitlePlaceHolder()}
                  autoComplete="off"
                  value={this.settings.title}
                  onChange={this.handleNameChange}
                />
              </Row>
              <Row>{this.renderChart()}</Row>
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

// Returns series data depending on the chart type,
// as each chart type expects data in a certain way.
// For example, a pie chart only expect one variable,
// whereas a bar chart expect two.
export function generateSeries(chartType, options) {
  switch (chartType) {
    case 'bar':
      return GenerateBarSeries(options, options.data)

    case 'line':
      return GenerateLineSeries(options, options.data)

    case 'pie':
      return GeneratePieSeries(options, options.data)

    case 'histogram':
      return GenerateHistogramSeries(options, options.data)

    default:
      throw Error(
        'visualization settings incorrect settings: {' + this.settings + '}'
      )
  }
}

export default SingleVisualization
