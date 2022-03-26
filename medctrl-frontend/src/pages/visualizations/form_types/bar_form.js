import React, { Component } from "react";

class BarForm extends Component {
  constructor(props) {
		super(props);

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

		this.state = {
      eligibleVariables: eligibleVariables,
      xAxis: "DecisionYear",
      yAxis: "Rapporteur",
			stacked: false,
			stackType: "100%",
			horizontal: false,
      categoriesSelected: []
		}

    this.handleChange = this.handleChange.bind(this);
    this.handleCategorySelection = this.handleCategorySelection.bind(this);
	}

  handleChange(event) {
    const target = event.target;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const name = target.name;
    this.setState({[name]: value}, () => {
      this.props.onChange([this.state, name]);
    });
  }

  handleCategorySelection(event) {
    const target = event.target;
    const value = target.checked;
    const name = target.name;
    if (value) {
      this.setState((state, props) => ({
        categoriesSelected: [...state.categoriesSelected, name]}),
         () => this.props.onChange([this.state, "categoriesSelected"]));
    }
    else {
      if (this.state.categoriesSelected.includes(name)) {
        this.setState((state, props) => ({
          categoriesSelected: state.categoriesSelected.filter((el) => 
            el !== name
          )
        }), () => this.props.onChange([this.state, "categoriesSelected"]));
      }
    }

  }

  renderCategoryOptions(Axis) {
    const options = this.props.uniqueCategories[Axis];
    return (options.map((option) => {
      return (
        <React.Fragment key={option}>
          <label>
            show {option}
            <input type="checkbox"
                   name={option}
                   checked={this.state.categoriesSelected.name}
                   onChange={this.handleCategorySelection} />
          </label>
          <br />
        </React.Fragment>
        
      )
    }))
  }

  renderVariableCheckBox() {
    return this.state.eligibleVariables.map((variable) => {
      return (<option key={variable} value={variable}>{variable}</option>);
    });
  }

	render() {
    let x_axis;
    let y_axis;

		if (this.state.horizontal) {
			x_axis = <React.Fragment>Y Axis</React.Fragment>
			y_axis = <React.Fragment>X Axis</React.Fragment>
		}
		else {
			x_axis = <React.Fragment>X Axis</React.Fragment>
			y_axis = <React.Fragment>Y Axis</React.Fragment>
		}

    const variablesXAxis = this.renderVariableCheckBox();
    const variablesYAxis = this.renderVariableCheckBox();
		
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
          Stack type

        </label>
        <br />
        <div style={{backgroundColor: "whitesmoke", height: "100px", overflowY: "scroll"}}>
          {this.renderCategoryOptions(this.state.yAxis)}
        </div>

      </React.Fragment>

    );
  }

}

export default BarForm