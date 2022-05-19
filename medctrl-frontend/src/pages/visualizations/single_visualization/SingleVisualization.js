// external imports
import React from 'react'
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
function SingleVisualization(props) {
  // initializing 'state' of the visualization
  let settings = props.settings

  // event handlers
  const handleChange = handleChangeFunction.bind(this)
  const handlePNGExport = handlePNGExportFunction.bind(this)
  const handleSVGExport = handleSVGExportFunction.bind(this)
  const handleRemoval = handleRemovalFunction.bind(this)
  const handleNameChange = handleNameChangeFunction.bind(this)

  // EVENT HANDLERS:

  // event handler for the 'form' data
  function handleChangeFunction(event) {
    settings.chartType = event.chartType
    settings.chartSpecificOptions = event.chartSpecificOptions
    settings.legendOn = event.legendOn
    settings.labelsOn = event.labelsOn

    props.onFormChangeFunc(settings)
  }

  // handles the png export
  function handlePNGExportFunction(event) {
    const title = settings.title ?? renderTitlePlaceHolder()
    HandlePNGExport(props.id, title, ApexCharts)
  }

  // handles the svg export
  function handleSVGExportFunction(event) {
    const title = settings.title ?? renderTitlePlaceHolder()
    HandleSVGExport(props.id, title, ApexCharts)
  }

  // handles the removal of this visualization
  function handleRemovalFunction(event) {
    props.onRemoval(props.settings.id, event)
  }

  // handles changing the title of the visualization
  // reacts to every keystroke, which is quite inefficient,
  // as it redraws the whole visualization
  function handleNameChangeFunction(event) {
    settings.title = event.target.value
    props.onFormChangeFunc(settings)
  }

  // GENERAL FUNCTIONS:

  // creating a chart based on the chosen chart type
  function renderChart() {
    const legendOn = settings.legendOn
    const labelsOn = settings.labelsOn
    const id = props.id
    const key = props.keys[id]
    const series = props.series[id]
    const categories = sortCategoryData(
      settings.chartSpecificOptions.categoriesSelectedX
    )
    const options = settings.chartSpecificOptions
    const onDataClick = props.onDataClick

    switch (settings.chartType) {
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
          'visualization settings incorrect settings: {' + settings + '}'
        )
    }
  }

  // renders the placeholder for the title depending on the chart type
  function renderTitlePlaceHolder() {
    const chartType = 'my ' + settings.chartType
    switch (settings.chartType) {
      case 'bar':
        return (
          chartType +
          ' - ' +
          settings.chartSpecificOptions.xAxis +
          ' vs ' +
          settings.chartSpecificOptions.yAxis
        )

      case 'line':
        return (
          chartType +
          ' - ' +
          settings.chartSpecificOptions.xAxis +
          ' vs ' +
          settings.chartSpecificOptions.yAxis
        )

      case 'pie':
        return chartType + ' - ' + settings.chartSpecificOptions.xAxis

      case 'histogram':
        return chartType + ' - ' + settings.chartSpecificOptions.xAxis

      default:
        throw Error(
          'visualization settings incorrect settings: {' + settings + '}'
        )
    }
  }

  // RENDERER:

  // Renders a single visualization,
  // based on the layout from the prototype:
  // divides the visualization in a left part for the 'form',
  // a right-lower part for the visualization and
  // a right-upper part for the filters.
  return (
    <div className="med-content-container visual-container">
      <Container>
        <Row>
          <Col className="visualization-panel">
            <VisualizationForm
              uniqueCategories={settings.uniqueCategories}
              onChange={handleChange}
              settings={settings}
            />
          </Col>
          <Col sm={8}>
            <Row>
              <input
                tour="step-vis-main"
                type="text"
                id={'graphName' + props.id}
                className="graph-name med-text-input"
                placeholder={renderTitlePlaceHolder()}
                autoComplete="off"
                value={settings.title}
                onChange={handleNameChange}
              />
            </Row>
            <Row>{renderChart()}</Row>
            <Row>
              <button
                className="med-primary-solid med-bx-button button-export"
                onClick={handlePNGExport}
              >
                <i className="bx bx-save filter-Icon"></i>Export as PNG
              </button>
              <button
                className="med-primary-solid med-bx-button button-export"
                onClick={handleSVGExport}
              >
                <i className="bx bx-save filter-Icon"></i>Export as SVG
              </button>
              <button
                className="med-primary-solid med-bx-button button-remove"
                onClick={handleRemoval}
                value={props.id}
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
      throw Error('visualization settings incorrect settings')
  }
}

export default SingleVisualization
