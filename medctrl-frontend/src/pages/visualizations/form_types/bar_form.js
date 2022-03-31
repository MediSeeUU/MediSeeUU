import React, { Component } from 'react'

import CategoryOptions from '../CategoryOptions'

// the bar part of a form if a bar chart is chosen
class BarForm extends Component {
  constructor(props) {
    // Receives the categories of all variables,
    // also gets the event handler for passing data back to the general form.
    super(props)

    // The list of eligible variables.
    // If we do not want to include a variable for the bar chart,
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

    // initialization of the state
    this.state = {
      eligibleVariables: eligibleVariables,
      xAxis: 'DecisionYear',
      yAxis: 'Rapporteur',
      stacked: false,
      stackType: false,
      horizontal: false,
      categoriesSelected: [],
    }

    // event handlers
    this.handleChange = this.handleChange.bind(this)
    this.handleCategorySelectionChange =
      this.handleCategorySelectionChange.bind(this)
  }

  // Updates the state,
  // then passes it to the general form.
  handleChange(event) {
    const target = event.target
    const value = target.type === 'checkbox' ? target.checked : target.value
    const name = target.name
    if (name === 'xAxis' || name === 'yAxis') {
      this.setState({ categoriesSelected: [] })
    }
    this.setState({ [name]: value }, () => {
      this.props.onChange([this.state, name])
    })
  }

  // Updates the categoriesSelected based on the new selection.
  // This event is passed to the CategoryOptions component.
  handleCategorySelectionChange(event) {
    this.setState({ categoriesSelected: event }, () => {
      this.props.onChange([this.state, 'categoriesSelected'])
    })
  }

  // creates a drop down menu based on the allowed variables
  renderVariableDropDown() {
    return this.state.eligibleVariables.map((variable) => {
      return (
        <option key={variable} value={variable}>
          {variable}
        </option>
      )
    })
  }

  // renders the bar form part of the form
  render() {
    let x_axis
    let y_axis

    // the x/y axis can change, it is easier to just change the labels
    if (this.state.horizontal) {
      x_axis = <React.Fragment>Y Axis</React.Fragment>
      y_axis = <React.Fragment>X Axis</React.Fragment>
    } else {
      x_axis = <React.Fragment>X Axis</React.Fragment>
      y_axis = <React.Fragment>Y Axis</React.Fragment>
    }

    // building drop down menus
    const variablesXAxis = this.renderVariableDropDown()
    const variablesYAxis = this.renderVariableDropDown()

    return (
      <React.Fragment>
        <label>
          {x_axis} <br />
          <select
            value={this.state.xAxis}
            name="xAxis"
            onChange={this.handleChange}
          >
            {variablesXAxis}
          </select>
        </label>
        <br />
        <label>
          {y_axis} <br />
          <select
            value={this.state.yAxis}
            name="yAxis"
            onChange={this.handleChange}
          >
            {variablesYAxis}
          </select>
        </label>
        <br />
        <label>
          Stacked
          <input
            type="checkbox"
            name="stacked"
            checked={this.state.stacked}
            onChange={this.handleChange}
          />
        </label>
        <br />
        <label>
          Stack fully
          <input
            type="checkbox"
            name="stackType"
            checked={this.state.stackType}
            onChange={this.handleChange}
          />
        </label>
        <br />
        <label>
          Horizontal
          <input
            type="checkbox"
            name="horizontal"
            checked={this.state.horizontal}
            onChange={this.handleChange}
          />
        </label>
        <br />
        <CategoryOptions
          key={`${this.state.xAxis}${this.state.yAxis}`}
          onChange={this.handleCategorySelectionChange}
          categories={this.props.uniqueCategories[this.state.yAxis]}
        />
      </React.Fragment>
    )
  }
}

export default BarForm
