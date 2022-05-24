import React from 'react'
import '../../../visualizations.css'
import CategoryOptions from '../shared/CategoryOptions'
import sortCategoryData from '../../utils/SortCategoryData'
import { eligibleVariablesVisualizations } from '../shared/eligibleVariables'

// the pie part of a form if a pie chart is chosen
function PieForm(props) {
  // The list of eligible variables.
  // If we do not want to include a variable for the pie chart,
  // it can be removed from here.
  const eligibleVariables = eligibleVariablesVisualizations()

  // initialization of the settings
  let settings = props.chartSpecificOptions

  // event handlers
  const handleChange = handleChangeFunc.bind(this)

  // EVENT HANDLERS:

  // Updates the settings,
  // then passes it to the general form.
  function handleChangeFunc(event) {
    const target = event.target
    const value = target.value
    const name = target.name

    settings[name] = value
    // the new settings is sent to the rest of the programme
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

  return (
    <>
      <label className="visualization-panel-label">
        Variable <br />
        <select
          value={settings.xAxis}
          name="xAxis"
          className="med-select"
          onChange={handleChange}
        >
          {renderVariableDropDown()}
        </select>
      </label>
      <div>
        <CategoryOptions
          dimension="X"
          className="category-options"
          onChange={handleChange}
          categories={sortCategoryData(props.uniqueCategories[settings.xAxis])}
          categoriesSelected={settings.categoriesSelectedX}
          settings={settings}
        />
      </div>
    </>
  )
}

export default PieForm
