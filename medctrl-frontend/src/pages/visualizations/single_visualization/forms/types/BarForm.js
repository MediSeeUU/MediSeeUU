// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'
import '../../../visualizations.css'
import sortCategoryData from '../../utils/sortCategoryData'
import CategoryOptions from '../shared/CategoryOptions'
import VariableSelect from '../../../../../shared/VariableSelect'

// the bar part of a form if a bar chart is chosen
function BarForm(props) {
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

  // GENERAL FUNCTIONS:

  // Renders the option to change the stack type,
  // only shown when the stacked option has been selected.
  function renderStackType() {
    return (
      <label className="med-vis-settings-panel-label">
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
      <label className="med-vis-settings-panel-label">
        <input
          type="checkbox"
          name="stacked"
          checked={settings.stacked}
          onChange={handleChange}
        />
        &nbsp;&nbsp;Stacked
      </label>
      {settings.stacked && renderStackType()}
      <label className="med-vis-settings-panel-label">
        <input
          type="checkbox"
          name="horizontal"
          checked={settings.horizontal}
          onChange={handleChange}
        />
        &nbsp;&nbsp;Switch axes
      </label>
      <div tour="step-vis-vars">
        <label className="med-vis-settings-panel-label">
          {xAxis}
          <VariableSelect
            className={'med-select'}
            defaultValue={settings.xAxis}
            name="xAxis"
            onChange={handleChange}
          />
        </label>
        <label className="med-vis-settings-panel-label">
          {yAxis}
          <VariableSelect
            className={'med-select'}
            defaultValue={settings.yAxis}
            name="yAxis"
            onChange={handleChange}
          />
        </label>
      </div>
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

export default BarForm
