import React from 'react'
import '../../../visualizations.css'
import CategoryOptions from '../shared/CategoryOptions'
import sortCategoryData from '../../utils/SortCategoryData'

// the pie part of a form if a pie chart is chosen
function PieForm(props) {
  // The list of eligible variables.
  // If we do not want to include a variable for the pie chart,
  // it can be removed from here.
  const eligibleVariables = [
    'ApplicationNo',
    'EUNumber',
    'EUNoShort',
    'BrandName',
    'MAH',
    'ActiveSubstance',
    'DecisionDate',
    'DecisionYear',
    'Period',
    'Rapporteur',
    'CoRapporteur',
    'ATCCodeL2',
    'ATCCodeL1',
    'ATCNameL2',
    'LegalSCope',
    'ATMP',
    'OrphanDesignation',
    'NASQualified',
    'CMA',
    'AEC',
    'LegalType',
    'PRIME',
    'NAS',
    'AcceleratedGranted',
    'AcceleratedExecuted',
    'ActiveTimeElapsed',
    'ClockStopElapsed',
    'TotalTimeElapsed',
  ]

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

    // The categories depend on which variables you chose,
    // so if these changes we want the categoriesSelected to re-initialized,
    // in this case that is just resetting the array,
    // because some variables have a lot of categories.
    if (name === 'xAxis') {
      settings.categoriesSelectedX = []
    }
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

  // renders the pie form part of the form
  const variables = renderVariableDropDown()

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
          {variables}
        </select>
      </label>
      <CategoryOptions
        // We want to reset the component when the variable changes,
        // so we need to change the key depending on the axis.
        key={`${settings.xAxis}`}
        dimension="X"
        className="category-options"
        onChange={handleChange}
        categories={sortCategoryData(props.uniqueCategories[settings.xAxis])}
        categoriesSelected={settings.categoriesSelectedX}
        settings={settings}
      />
    </>
  )
}

export default PieForm
