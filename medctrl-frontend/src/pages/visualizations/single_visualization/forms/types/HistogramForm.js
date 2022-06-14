import React from 'react'
import '../../../visualizations.css'
import CategoryOptions from '../shared/CategoryOptions'
import sortCategoryData from '../../utils/sortCategoryData'
import VariableSelect from '../../../../../shared/VariableSelect'

// the histogram part of a form if a histogram chart is chosen
function HistogramForm(props) {
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

    // if we change a variable, we also need to show new categories to be selected
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

  // RENDERER:

  // renders the histogram form part of the form
  return (
    <>
      <label className="med-vis-settings-panel-label">
        Variable <br />
        <VariableSelect
          className={'med-select'}
          defaultValue={settings.xAxis}
          name="xAxis"
          onChange={handleChange}
          tour="step-vis-vars"
        />
      </label>
      <div tour="step-vis-categories">
        <CategoryOptions
          dimension="X"
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
