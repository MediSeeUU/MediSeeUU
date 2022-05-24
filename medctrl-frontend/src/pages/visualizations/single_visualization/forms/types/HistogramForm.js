import React from 'react'
import '../../../visualizations.css'
import CategoryOptions from '../shared/CategoryOptions'
import sortCategoryData from '../../utils/SortCategoryData'
import { eligibleVariablesVisualizations } from '../shared/eligibleVariables'

// the histogram part of a form if a histogram chart is chosen
function HistogramForm(props) {
  // The list of eligible variables.
  // If we do not want to include a variable for the histogram chart,
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

    if (name === 'xAxis') {
      settings.categoriesSelectedX = props.uniqueCategories[value]
    }

    settings[name] = value
    props.onChange({
      target: {
        type: 'array',
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

  // renders the histogram form part of the form
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

export default HistogramForm
