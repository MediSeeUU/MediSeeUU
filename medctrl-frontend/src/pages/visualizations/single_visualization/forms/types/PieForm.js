import React, { Component } from 'react'
import '../../../visualizations.css'
import CategoryOptions from '../shared/CategoryOptions'

// the pie part of a form if a pie chart is chosen
class PieForm extends Component {
  constructor(props) {
    /* 
      Receives the categories of all variables,
      also gets the event handler for passing data back to the general form.
    */
    super(props)

    /*
      The list of eligible variables.
      If we do not want to include a variable for the pie chart,
      it can be removed from here.
    */
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
      chosenVariable: 'Rapporteur',
      categoriesSelected: [],
    }

    // event handlers
    this.handleChange = this.handleChange.bind(this)
    this.handleCategorySelectionChange =
      this.handleCategorySelectionChange.bind(this)
  }

  // EVENT HANDLERS:

  /*
    Updates the state,
    then passes it to the general form.
  */
  handleChange(event) {
    const target = event.target
    const value = target.type === 'checkbox' ? target.checked : target.value
    const name = target.name

    /* 
      the categories depend on which variables you chose,
      so if these changes we want the categoriesSelected to re-initialized,
      in this case that is just resetting the array
    */
    if (name === 'chosenVariable') {
      this.setState({ categoriesSelected: [] })
    }
    this.setState({ [name]: value }, () => {
      this.props.onChange([this.state, name])
    })
  }

  /* 
    Updates the categoriesSelected based on the new selection.
    This event is passed to the CategoryOptions component.
  */
  handleCategorySelectionChange(event) {
    this.setState({ categoriesSelected: event }, () => {
      this.props.onChange([this.state, 'categoriesSelected'])
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
            value={this.state.chosenVariable}
            name="chosenVariable"
            onChange={this.handleChange}
          >
            {variables}
          </select>
        </label>
        <br />
        <CategoryOptions
          /* 
            We want to reset the component when the variable changes,
            may need to become an increment function
          */
          key={`${this.state.chosenVariabe}`}
          className="category-options"
          onChange={this.handleCategorySelectionChange}
          categories={this.props.uniqueCategories[this.state.chosenVariable]}
        />
      </React.Fragment>
    )
  }
}

export default PieForm
