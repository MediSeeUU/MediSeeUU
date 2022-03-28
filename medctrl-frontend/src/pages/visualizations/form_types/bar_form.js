import React, { Component } from "react";

// the bar part of a form if a bar chart is chosen
class BarForm extends Component {
  constructor(props) {
		super(props);

    // the list of eligible variables
    // if we do not want to include a variable for the bar chart,
    // it can be removed from here
    const eligibleVariables = [
      "ApplicationNo",
      "EUNumber",
      "EUNoShort",
      "BrandName",
      "MAH",
      "ActiveSubstance",
      "DecisionDate",
      "DecisionYear",
      "Period",
      "Rapporteur",
      "CoRapporteur",
      "ATCCodeL2",
      "ATCCodeL1",
      "ATCNameL2",
      "LegalSCope",
      "ATMP",
      "OrphanDesignation",
      "NASQualified",
      "CMA",
      "AEC",
      "LegalType",
      "PRIME",
      "NAS",
      "AcceleratedGranted",
      "AcceleratedExecuted",
      "ActiveTimeElapsed",
      "ClockStopElapsed",
      "TotalTimeElapsed"
    ]

    // initialization of the state
		this.state = {
      eligibleVariables: eligibleVariables,
      xAxis: "DecisionYear",
      yAxis: "Rapporteur",
			stacked: false,
			stackType: false,
			horizontal: false,
      categoriesSelected: []
		}

    // event handlers
    this.handleChange = this.handleChange.bind(this);
    this.handleCategorySelection = this.handleCategorySelection.bind(this);
	}

  // updates the state,
  // then passes it to the general form
  handleChange(event) {
    const target = event.target;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const name = target.name;
    this.setState({[name]: value}, () => {
      this.props.onChange([this.state, name]);
    });
  }

  // updating what categories have been selected,
  // then passes it to the general form
  handleCategorySelection(event) {
    const target = event.target;
    const value = target.checked;
    const name = target.name;

    // if the category has been selected,
    // add it to the list of selected categories
    if (value) {
      this.setState(state => ({
        categoriesSelected: [...state.categoriesSelected, name]}),
         () => this.props.onChange([this.state, "categoriesSelected"]));
    }
    else {
      // remove if the category was previously on the list,
      if (this.state.categoriesSelected.includes(name)) {
        this.setState(state => ({
          categoriesSelected: state.categoriesSelected.filter(el => 
            el !== name
          )
        }), () => this.props.onChange([this.state, "categoriesSelected"]));
      }
    }
  }

  // create the list of category checkboxes
  renderCategoryOptions(Axis) {
    const categories = this.props.uniqueCategories[Axis];
    return (categories.map(category => {
      return (
        <React.Fragment key={category}>
          <label>
            show {category}
            <input type="checkbox"
                   name={category}
                   checked={this.state.categoriesSelected.includes(category)}
                   onChange={this.handleCategorySelection} />
          </label>
          <br />
        </React.Fragment>       
      );
    }));
  }

  // creates a drop down menu based on the allowed variables
  renderVariableDropDown() {
    return this.state.eligibleVariables.map((variable) => {
      return (<option key={variable} value={variable}>{variable}</option>);
    });
  }

  // renders the bar form part of the form
	render() {
    let x_axis;
    let y_axis;

    // the x/y axis can change, it is easier to just change the labels
		if (this.state.horizontal) {
			x_axis = <React.Fragment>Y Axis</React.Fragment>
			y_axis = <React.Fragment>X Axis</React.Fragment>
		}
		else {
			x_axis = <React.Fragment>X Axis</React.Fragment>
			y_axis = <React.Fragment>Y Axis</React.Fragment>
		}

    const variablesXAxis = this.renderVariableDropDown();
    const variablesYAxis = this.renderVariableDropDown();
		
    return (
      <React.Fragment>
        <label>
          {x_axis} <br />
          <select value={this.state.xAxis} 
                  name="xAxis" 
                  onChange={this.handleChange}>
            {variablesXAxis}
          </select>
        </label>
        <br />
				<label>
          {y_axis} <br />
          <select value={this.state.yAxis} 
                  name="yAxis" 
                  onChange={this.handleChange}>
            {variablesYAxis}
          </select>
        </label>
        <br />
        <label>
          Stacked
          <input type="checkbox"
                 name="stacked"
                 checked={this.state.stacked}
                 onChange={this.handleChange} />
        </label>
        <br />
        <label>
          Stack fully
          <input type="checkbox"
                 name="stackType"
                 checked={this.state.stackType}
                 onChange={this.handleChange} />
        </label>
        <br />
        <label>
          Horizontal
          <input type="checkbox"
                 name="horizontal"
                 checked={this.state.horizontal}
                 onChange={this.handleChange} />
        </label>
        <br />
        <div style={{backgroundColor: "whitesmoke", 
                     height: "100px", 
                     overflowY: "scroll"}}>
          {this.renderCategoryOptions(this.state.yAxis)}
        </div>
      </React.Fragment>
    );
  }
}

export default BarForm