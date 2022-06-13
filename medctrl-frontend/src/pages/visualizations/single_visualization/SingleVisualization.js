// external imports
import React from 'react'
import Col from 'react-bootstrap/Col'
import Row from 'react-bootstrap/Row'
import Container from 'react-bootstrap/Container'
import ApexCharts from 'apexcharts'

// internal imports
import VisualizationForm from './forms/VisualizationForm'
import BarChart from './visualization_types/BarChart'
import LineChart from './visualization_types/LineChart'
import PieChart from './visualization_types/PieChart'
import HistogramChart from './visualization_types/HistogramChart'
import HandleSVGExport from './exports/HandleSVGExport'
import HandlePNGExport from './exports/HandlePNGExport'
import sortCategoryData from './utils/sortCategoryData'
import generateSeries from './utils/generateSeries'

// Renders the components for a single visualization.
// There are multiple chart types, which can have different options.
// Therefore there are separate components for forms and interfaces.
// Currently there tends not to be huge differences though.
function SingleVisualization(props) {
  // Initializing 'state' of the visualization.
  // A normal variable was preferred over state,
  // as state cannot ordinarily be re-initialized when new props have been sent
  // Although keys or certain lifetime methods can also be used.
  let settings = props.settings

  // Filter out the selected categories that are not present anymore in the data categories
  // Selected categories can disappear because of data that is deselected in the popup
  settings.chartSpecificOptions.categoriesSelectedX =
    settings.chartSpecificOptions.categoriesSelectedX.filter((e) =>
      settings.uniqueCategories[settings.chartSpecificOptions.xAxis].includes(e)
    )
  settings.chartSpecificOptions.categoriesSelectedY =
    settings.chartSpecificOptions.categoriesSelectedY.filter((e) =>
      settings.uniqueCategories[settings.chartSpecificOptions.yAxis].includes(e)
    )

  // event handlers
  const handleChange = handleChangeFunction.bind(this)
  const handlePNGExport = handlePNGExportFunction.bind(this)
  const handleSVGExport = handleSVGExportFunction.bind(this)
  const handleRemoval = handleRemovalFunction.bind(this)
  const handleTitleChange = handleTitleChangeFunction.bind(this)

  // EVENT HANDLERS:

  // event handler for the 'form' data
  function handleChangeFunction(name, value) {
    settings[name] = value
    props.onFormChangeFunc(settings)
  }

  // handles the png export
  function handlePNGExportFunction(event) {
    const title = settings.title ?? renderTitlePlaceHolder()
    HandlePNGExport(settings.id, title, ApexCharts)
  }

  // handles the svg export
  function handleSVGExportFunction(event) {
    HandleSVGExport(settings.id, ApexCharts)
  }

  // handles the removal of this visualization
  function handleRemovalFunction(event) {
    props.onRemoval(settings.id, event)
  }

  // Handles changing the title of the visualization.
  // Currently the title is not added when a visualization is exported,
  // this would require the title to be propagated to the chart options.
  // It would also require the text input to be put in the form,
  // otherwise 2 titles would be placed below each other.
  function handleTitleChangeFunction(event) {
    settings.title = event.target.value
    props.onFormChangeFunc(settings)
  }

  // GENERAL FUNCTIONS:

  // creating a chart based on the chosen chart type
  function renderChart() {
    const legendOn = settings.legendOn
    const labelsOn = settings.labelsOn
    const id = settings.id
    const options = settings.chartSpecificOptions
    const onDataClick = props.onDataClick

    // The index of a category in categories needs to correspond with
    // their equivalent in series, so we sort them.
    // The series are sorted in their respective interfaces as well.
    const series = generateSeries(settings)
    const categories = sortCategoryData(
      settings.chartSpecificOptions.categoriesSelectedX
    )

    switch (settings.chartType) {
      case 'bar':
        return (
          <BarChart
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

  // renders the placeholder for the title
  function renderTitlePlaceHolder() {
    const base =
      'my ' + settings.chartType + ' - ' + settings.chartSpecificOptions.xAxis

    switch (settings.chartType) {
      case 'bar':
        return base + ' vs ' + settings.chartSpecificOptions.yAxis

      case 'line':
        return base + ' vs ' + settings.chartSpecificOptions.yAxis

      default:
        return base
    }
  }

  // RENDERER:

  // Renders a single visualization
  // divides the visualization into:
  // - a left part for the 'form',
  // - a right-upper part for the title
  // - a right-middle part for the visualization
  // - a right-lower part for the exports and a remove button
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
                defaultValue={settings.title || ''}
                onBlur={handleTitleChange}
              />
            </Row>
            <div tour="step-vis-plot">
              <Row>{renderChart()}</Row>
            </div>
            <Row>
              <button
                className="med-primary-solid med-bx-button button-export"
                onClick={handlePNGExport}
              >
                <i className="bx bx-save med-button-image"></i>Export as PNG
              </button>
              <button
                className="med-primary-solid med-bx-button button-export"
                onClick={handleSVGExport}
              >
                <i className="bx bx-save med-button-image"></i>Export as SVG
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

export default SingleVisualization
