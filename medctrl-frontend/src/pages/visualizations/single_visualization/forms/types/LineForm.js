import React from 'react'
import '../../../visualizations.css'
import sortCategoryData from '../../utils/SortCategoryData'
import CategoryOptions from '../shared/CategoryOptions'
import VariableSelect from '../../../../../shared/VariableSelect'

// the line part of a form if a line chart is chosen
function LineForm(props) {
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

    // if we change a variable, we also need to show new categories to be selected
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

  // RENDERER:

  // renders the bar form part of the form
  return (
    <>
      <label className="visualization-panel-label">
        X-axis
        <VariableSelect
          className={'med-select'}
          defaultValue={settings.xAxis}
          name="xAxis"
          onChange={handleChange}
        />
      </label>
      <label className="visualization-panel-label">
        Y-axis
        <VariableSelect
          className={'med-select'}
          defaultValue={settings.yAxis}
          name="yAxis"
          onChange={handleChange}
        />
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
