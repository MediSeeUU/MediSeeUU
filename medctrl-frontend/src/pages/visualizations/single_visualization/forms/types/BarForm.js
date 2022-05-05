import React, { Component } from 'react'
import '../../../visualizations.css'
import sortCategoryData from '../../utils/SortCategoryData'
import CategoryOptions from '../shared/CategoryOptions'

// the bar part of a form if a bar chart is chosen
class BarForm extends Component {
  constructor(props) {
    // Receives the unique categories of all variables,
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
    this.state = this.props.chartSpecificOptions
    this.state.eligibleVariables = eligibleVariables

    // event handlers
    this.handleChange = this.handleChange.bind(this)
    this.handleCategorySelectionXChange =
      this.handleCategorySelectionXChange.bind(this)
    this.handleCategorySelectionYChange =
      this.handleCategorySelectionYChange.bind(this)
  }

  // EVENT HANDLERS:

  // Updates the state,
  // then passes it to the general form.
  handleChange(event) {
    const target = event.target
    const value = target.type === 'checkbox' ? target.checked : target.value
    const name = target.name

    // the categories depend on which variables you chose,
    // so if these change we want the categoriesSelected to re-initialized,
    // in this case that is just resetting the array,
    // because some variables have a lot of categories
    if (name === 'xAxis' || name === 'yAxis') {
      this.setState({
        categoriesSelectedX: [],
        categoriesSelectedY: [],
      })
    }
    this.setState({ [name]: value }, () => {
      this.props.onChange([this.state, name])
    })
  }

  // Updates the categoriesSelectedX based on the new selection.
  // This event handler is passed to the CategoryOptions component.
  handleCategorySelectionXChange(event) {
    this.setState({ categoriesSelectedX: event }, () => {
      this.props.onChange([this.state, 'categoriesSelectedX'])
    })
  }

  // Updates the categoriesSelectedY based on the new selection.
  // This event handler is passed to the CategoryOptions component.
  handleCategorySelectionYChange(event) {
    this.setState({ categoriesSelectedY: event }, () => {
      this.props.onChange([this.state, 'categoriesSelectedY'])
    })
  }

  // GENERAL FUNCTIONS:

  // creates a drop down menu based on the eligible variables
  renderVariableDropDown() {
    return this.state.eligibleVariables.map((variable) => {
      return (
        <option key={variable} value={variable}>
          {variable}
        </option>
      )
    })
  }

  // renders the option to change the stack type
  // only shown when the stacked option has been selected
  renderStackType() {
    return (
      <label className="visualization-panel-label">
        <input
          type="checkbox"
          name="stackType"
          checked={this.state.stackType}
          onChange={this.handleChange}
        />
        &nbsp;&nbsp;Stack fully
      </label>
    )
  }

  // RENDERER:

  // renders the bar form part of the form
  render() {
    let xAxis
    let yAxis

    // the x/y axis can change, it is easier to just change the labels
    if (this.state.horizontal) {
      xAxis = <React.Fragment>Y-axis</React.Fragment>
      yAxis = <React.Fragment>X-axis</React.Fragment>
    } else {
      xAxis = <React.Fragment>X-axis</React.Fragment>
      yAxis = <React.Fragment>Y-axis</React.Fragment>
    }

    // building drop down menus
    const variablesXAxis = this.renderVariableDropDown()
    const variablesYAxis = this.renderVariableDropDown()

    return (
      <React.Fragment>
        <label className="visualization-panel-label">
          <input
            type="checkbox"
            name="stacked"
            checked={this.state.stacked}
            onChange={this.handleChange}
          />
          &nbsp;&nbsp;Stacked
        </label>
        {this.state.stacked && this.renderStackType()}
        <label className="visualization-panel-label">
          <input
            type="checkbox"
            name="horizontal"
            checked={this.state.horizontal}
            onChange={this.handleChange}
          />
          &nbsp;&nbsp;Horizontal
        </label>
        <label className="visualization-panel-label">
          {xAxis}
          <select
            className="med-select"
            value={this.state.xAxis}
            name="xAxis"
            onChange={this.handleChange}
          >
            {variablesXAxis}
          </select>
        </label>
        <label className="visualization-panel-label">
          {yAxis}
          <select
            className="med-select"
            value={this.state.yAxis}
            name="yAxis"
            onChange={this.handleChange}
          >
            {variablesYAxis}
          </select>
        </label>
        <CategoryOptions
          // We want to reset the component when the axis changes,
          // so we need to change the key depending on the axis'.
          key={`${this.state.xAxis}${this.state.yAxis}` + 'X'}
          className="category-options"
          onChange={this.handleCategorySelectionXChange}
          categories={sortCategoryData(
            this.props.uniqueCategories[this.state.xAxis]
          )}
          categoriesSelected={this.state.categoriesSelectedX}
          settings={this.state}
        />
        <CategoryOptions
          // We want to reset the component when the axis changes,
          // so we need to change the key depending on the axis'.
          key={`${this.state.xAxis}${this.state.yAxis}` + 'Y'}
          className="category-options"
          onChange={this.handleCategorySelectionYChange}
          categories={sortCategoryData(
            this.props.uniqueCategories[this.state.yAxis]
          )}
          categoriesSelected={this.state.categoriesSelectedY}
          settings={this.state}
        />
      </React.Fragment>
    )
  }
}

export default BarForm
