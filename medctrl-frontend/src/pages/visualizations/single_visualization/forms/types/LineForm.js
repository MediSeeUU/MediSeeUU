import React, { Component } from 'react'
import '../../../visualizations.css'
import sortCategoryData from '../../utils/SortCategoryData'
import CategoryOptions from '../shared/CategoryOptions'
import { v4 as uuidv4 } from 'uuid'

// the line part of a form if a line chart is chosen
class LineForm extends Component {
  constructor(props) {
    //  Receives the categories of all variables,
    //  also gets the event handler for passing data back to the general form.
    super(props)

    // The list of eligible variables.
    // If we do not want to include a variable for the line chart,
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
    const value = target.value
    const name = target.name

    // The categories depend on which variables you chose,
    // so if these changes we want the categoriesSelected to re-initialized,
    // in this case that is just resetting the array,
    // because some variables have a lot of categories.
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
      this.props.onChange([this.state, uuidv4()])
    })
  }

  // Updates the categoriesSelectedY based on the new selection.
  // This event is passed to the CategoryOptions component.
  handleCategorySelectionYChange(event) {
    this.setState({ categoriesSelectedY: event }, () => {
      this.props.onChange([this.state, uuidv4()])
    })
  }

  // GENERAL FUNCTIONS:

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

  // RENDERER:

  // renders the bar form part of the form
  render() {
    // building drop down menus
    const variablesXAxis = this.renderVariableDropDown()
    const variablesYAxis = this.renderVariableDropDown()

    return (
      <React.Fragment>
        <label className="visualization-panel-label">
          X-axis
          <select
            value={this.state.xAxis}
            name="xAxis"
            className="med-select"
            onChange={this.handleChange}
          >
            {variablesXAxis}
          </select>
        </label>
        <label className="visualization-panel-label">
          Y-axis
          <select
            value={this.state.yAxis}
            name="yAxis"
            className="med-select"
            onChange={this.handleChange}
          >
            {variablesYAxis}
          </select>
        </label>
        <CategoryOptions
          // We want to reset the component when the axis changes,
          // so we need to change the key depending on the axis'
          key={`${this.state.xAxis}${this.state.yAxis}` + 'X'}
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

export default LineForm
