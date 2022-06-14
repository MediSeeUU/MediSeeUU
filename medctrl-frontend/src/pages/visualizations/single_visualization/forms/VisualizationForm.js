import React from 'react'
import 'bootstrap/dist/css/bootstrap.min.css'

import BarForm from './types/BarForm'
import LineForm from './types/LineForm'
import PieForm from './types/PieForm'
import HistogramForm from './types/HistogramForm'

// form component for a single visualization
function VisualizationForm(props) {
  // initializing the settings
  let settings = {
    chartType: props.settings.chartType,
    legendOn: props.settings.legendOn,
    labelsOn: props.settings.labelsOn,
    chartSpecificOptions: props.settings.chartSpecificOptions,
  }

  // event handlers
  const handleChange = handleChangeFunc.bind(this)

  // EVENT HANDLERS:

  // Event handler for updating the settings after a single change.
  // This event can be a real event or just data passed from a child,
  // as this function is given as prop to form types.
  // Do note that if the chart type changes,
  // we still remember the previous options.
  function handleChangeFunc(event) {
    const target = event.target
    const value = target.type === 'checkbox' ? target.checked : target.value
    const name = target.name

    settings[name] = value
    props.onChange(name, value)
  }

  // GENERAL FUNCTIONS

  // renders the form for the chosen chart
  function renderChartOptions(chartType) {
    switch (chartType) {
      case 'bar':
        return (
          <BarForm
            uniqueCategories={props.uniqueCategories}
            onChange={handleChange}
            chartSpecificOptions={settings.chartSpecificOptions}
          />
        )

      case 'line':
        return (
          <LineForm
            uniqueCategories={props.uniqueCategories}
            onChange={handleChange}
            chartSpecificOptions={settings.chartSpecificOptions}
          />
        )

      case 'pie':
        return (
          <PieForm
            uniqueCategories={props.uniqueCategories}
            onChange={handleChange}
            chartSpecificOptions={settings.chartSpecificOptions}
          />
        )

      case 'histogram':
        return (
          <HistogramForm
            uniqueCategories={props.uniqueCategories}
            onChange={handleChange}
            chartSpecificOptions={settings.chartSpecificOptions}
          />
        )

      default:
        throw Error('form error: chart type is ineligible: {' + settings + '}')
    }
  }

  // RENDERER

  // render method for the form
  return (
    <div className="med-vis-settings-form">
      <label tour="step-vis-type" className="med-vis-settings-panel-label">
        Visualization type
        <select
          value={settings.chartType}
          name="chartType"
          className="med-select"
          onChange={handleChange}
        >
          <option value="bar">Bar chart - 2 variables</option>
          <option value="line">Line chart</option>
          <option value="pie">Pie chart</option>
          <option value="histogram">Bar chart - 1 variable</option>
        </select>
      </label>
      {renderChartOptions(settings.chartType)}
      <label className="med-vis-settings-panel-label">
        <input
          type="checkbox"
          name="legendOn"
          checked={settings.legendOn}
          onChange={handleChange}
        />
        &nbsp;&nbsp;Show legend
      </label>
      <label className="med-vis-settings-panel-label">
        <input
          type="checkbox"
          name="labelsOn"
          checked={settings.labelsOn}
          onChange={handleChange}
        />
        &nbsp;&nbsp;Show labels
      </label>
    </div>
  )
}

export default VisualizationForm
