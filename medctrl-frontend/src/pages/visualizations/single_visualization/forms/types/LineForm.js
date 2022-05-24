import React from 'react'
import '../../../visualizations.css'
import sortCategoryData from '../../utils/SortCategoryData'
import { eligibleVariablesVisualizations } from '../shared/eligibleVariables'
import CategoryOptions from '../shared/CategoryOptions'

// the line part of a form if a line chart is chosen
function LineForm(props) {
  // The list of eligible variables.
  // If we do not want to include a variable for the line chart,
  // it can be removed from here.
  const eligibleVariables = eligibleVariablesVisualizations()

  // initialization of the state
  let settings = props.chartSpecificOptions

  // event handlers
  const handleChange = handleChangeFunc.bind(this)

  // EVENT HANDLERS:

  // Updates the state,
  // then passes it to the general form.
  function handleChangeFunc(event) {
    const target = event.target
    const value = target.value
    const name = target.name

    if (name === 'xAxis') {
      settings.categoriesSelectedX = props.uniqueCategories[value]
    } else if (name === 'yAxis') {
      settings.categoriesSelectedY = props.uniqueCategories[value]
    }

    settings[name] = value
    props.onChange({
      target: {
        type: 'dict',
        value: settings,
        name: 'chartSpecificOptions',
      },
    })
  }

  // GENERAL FUNCTIONS:

  // creates a drop down menu based on the allowed variables
  function renderVariableDropDown() {
    return eligibleVariables.map((variable) => {
      return (
        <option key={variable} value={variable}>
          {variable}
        </option>
      )
    })
  }

  // RENDERER:

  // renders the bar form part of the form
  return (
    <>
      <label className="visualization-panel-label">
        X-axis
        <select
          value={settings.xAxis}
          name="xAxis"
          className="med-select"
          onChange={handleChange}
        >
          {renderVariableDropDown()}
        </select>
      </label>
      <label className="visualization-panel-label">
        Y-axis
        <select
          value={settings.yAxis}
          name="yAxis"
          className="med-select"
          onChange={handleChange}
        >
          {renderVariableDropDown()}
        </select>
      </label>
      <div>
        <CategoryOptions
          dimension="X"
          onChange={handleChange}
          categories={sortCategoryData(props.uniqueCategories[settings.xAxis])}
          categoriesSelected={settings.categoriesSelectedX}
          settings={settings}
        />
        <CategoryOptions
          dimension="Y"
          onChange={handleChange}
          categories={sortCategoryData(props.uniqueCategories[settings.yAxis])}
          categoriesSelected={settings.categoriesSelectedY}
          settings={settings}
        />
      </div>
    </>
  )
}

export default LineForm
