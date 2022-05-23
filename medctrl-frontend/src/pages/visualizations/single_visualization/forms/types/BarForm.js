import React from 'react'
import '../../../visualizations.css'
import sortCategoryData from '../../utils/SortCategoryData'
import { eligibleVariablesVisualizations } from '../shared/eligibleVariables'
import CategoryOptions from '../shared/CategoryOptions'

// the bar part of a form if a bar chart is chosen
function BarForm(props) {
  // The list of eligible variables.
  // If we do not want to include a variable for the bar chart,
  // it can be removed from here.
  let eligibleVariables = eligibleVariablesVisualizations()

  let settings = props.chartSpecificOptions

  // event handlers
  const handleChange = handleChangeFunc.bind(this)

  // EVENT HANDLERS:

  // Updates the settings,
  // then passes it to the general form.
  function handleChangeFunc(event) {
    const target = event.target
    const value = target.type === 'checkbox' ? target.checked : target.value
    const name = target.name

    // The categories depend on which variables you chose,
    // so if these change we want the categoriesSelected to re-initialized,
    // in this case that is just resetting the array,
    // because some variables have a lot of categories.
    if (name === 'xAxis' || name === 'yAxis') {
      settings.categoriesSelectedX = []
      settings.categoriesSelectedY = []
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

  // creates a drop down menu based on the eligible variables
  function renderVariableDropDown() {
    return eligibleVariables.map((variable) => {
      return (
        <option key={variable} value={variable}>
          {variable}
        </option>
      )
    })
  }

  // renders the option to change the stack type
  // only shown when the stacked option has been selected
  function renderStackType() {
    return (
      <label className="visualization-panel-label">
        <input
          type="checkbox"
          name="stackType"
          checked={settings.stackType}
          onChange={handleChange}
        />
        &nbsp;&nbsp;Stack fully
      </label>
    )
  }

  // RENDERER:

  let xAxis
  let yAxis

  // the x/y axis can change, it is easier to just change the labels
  if (settings.horizontal) {
    xAxis = <>Y-axis</>
    yAxis = <>X-axis</>
  } else {
    xAxis = <>X-axis</>
    yAxis = <>Y-axis</>
  }

  // renders the bar form part of the form
  return (
    <>
      <label className="visualization-panel-label">
        <input
          type="checkbox"
          name="stacked"
          checked={settings.stacked}
          onChange={handleChange}
        />
        &nbsp;&nbsp;Stacked
      </label>
      {settings.stacked && renderStackType()}
      <label className="visualization-panel-label">
        <input
          type="checkbox"
          name="horizontal"
          checked={settings.horizontal}
          onChange={handleChange}
        />
        &nbsp;&nbsp;Horizontal
      </label>
      <div tour="step-vis-vars">
        <label className="visualization-panel-label">
          {xAxis}
          <select
            className="med-select"
            value={settings.xAxis}
            name="xAxis"
            onChange={handleChange}
          >
            {renderVariableDropDown()}
          </select>
        </label>
        <label className="visualization-panel-label">
          {yAxis}
          <select
            className="med-select"
            value={settings.yAxis}
            name="yAxis"
            onChange={handleChange}
          >
            {renderVariableDropDown()}
          </select>
        </label>
      </div>
      <div tour="step-vis-categories">
        <CategoryOptions
          dimension="X"
          className="category-options"
          onChange={handleChange}
          categories={sortCategoryData(props.uniqueCategories[settings.xAxis])}
          categoriesSelected={settings.categoriesSelectedX}
          settings={settings}
        />
        <CategoryOptions
          dimension="Y"
          className="category-options"
          onChange={handleChange}
          categories={sortCategoryData(props.uniqueCategories[settings.yAxis])}
          categoriesSelected={settings.categoriesSelectedY}
          settings={settings}
        />
      </div>
    </>
  )
}

export default BarForm
