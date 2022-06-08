// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import React, { Component } from 'react'
import '../../../visualizations.css'
import CategoryOptions from '../shared/CategoryOptions'
import sortCategoryData from '../../utils/SortCategoryData'
import { v4 as uuidv4 } from 'uuid'

// the pie part of a form if a pie chart is chosen
class PieForm extends Component {
  constructor(props) {
    // Receives the categories of all variables,
    // also gets the event handler for passing data back to the general form.
    super(props)

    // The list of eligible variables.
    // If we do not want to include a variable for the pie chart,
    // it can be removed from here.
    const eligibleVariables = [
      'BrandName',
      'MAH',
      'ActiveSubstance',
      'DecisionDate',
      'DecisionYear',
      'ATCCodeL2',
      'ApplicationNo',
      'EUNoShort',
      'Rapporteur',
      'CoRapporteur',
      'ATMP',
      'OrphanDesignation',
      'NASQualified',
      'PRIME',
      'LegalSCope',
      'LegalType',
      'AcceleratedGranted',
      'AcceleratedExecuted',
      'ActiveTimeElapsed',
      'ClockStopElapsed',
      'TotalTimeElapsed',
    ]

    // initialization of the state
    let chartSpecificOptions = this.props.chartSpecificOptions
    chartSpecificOptions['eligibleVariables'] = eligibleVariables
    this.state = chartSpecificOptions

    // event handlers
    this.handleChange = this.handleChange.bind(this)
    this.handleCategorySelectionChange =
      this.handleCategorySelectionChange.bind(this)
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
    if (name === 'xAxis') {
      this.setState({ categoriesSelectedX: [] })
    }
    this.setState({ [name]: value }, () => {
      this.props.onChange([this.state, name])
    })
  }

  // Updates the categoriesSelected based on the new selection.
  // This event is passed to the CategoryOptions component.
  handleCategorySelectionChange(event) {
    this.setState({ categoriesSelectedX: event }, () => {
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

  // renders the pie form part of the form
  render() {
    // building drop down menus
    const variables = this.renderVariableDropDown()

    return (
      <React.Fragment>
        <label className="visualization-panel-label">
          Variable <br />
          <select
            value={this.state.xAxis}
            name="xAxis"
            className="med-select"
            onChange={this.handleChange}
          >
            {variables}
          </select>
        </label>
        <CategoryOptions
          // We want to reset the component when the variable changes,
          // so we need to change the key depending on the axis.
          key={`${this.state.xAxis}`}
          className="category-options"
          onChange={this.handleCategorySelectionChange}
          categories={sortCategoryData(
            this.props.uniqueCategories[this.state.xAxis]
          )}
          categoriesSelected={this.state.categoriesSelectedX}
          settings={this.state}
        />
      </React.Fragment>
    )
  }
}

export default PieForm
