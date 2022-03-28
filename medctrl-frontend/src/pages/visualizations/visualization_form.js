import React, { Component } from "react";
import 'bootstrap/dist/css/bootstrap.min.css';

import BarForm from "./form_types/bar_form";

// form component for a single visualization
class VisualizationForm extends Component {
  constructor(props) {
    super(props);

    // initializing the state, options are off to keep the start quick
    // the chartSpecificOptionsName is used for determining the key of 
    // the actual chart, to notigy the chart that it has been updated
    this.state = {chart_type: "bar", 
                  legend_on: false,
                  labels_on: false,
                  chartSpecificOptions: {},
                  chartSpecificOptionsName: ""}

    // event handlers
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChartSpecificChange = this.handleChartSpecificChange.bind(this);
  }

  // event handler for updating the state after a single selection 
  handleChange(event) {
    const target = event.target;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const name = target.name;
    this.setState({[name]: value});
  }

  // event handler for updating the state
  // after the chart specific options were altered
  // also updates which value was last updated
  handleChartSpecificChange(options) {
    this.setState({chartSpecificOptions: options[0], 
                   chartSpecificOptionsName: options[1]});
  }

  // event handler for the submission after all selections
  handleSubmit(event) {
    // makes sure that the page does not reload and thus resets the data
    event.preventDefault();
    // function passed down as a prop by SingleVisualization
    this.props.onFormChange(this.state);
  }

  // renders the form for the chosen chart
  renderChartOptions(chart_type) {
    switch (chart_type) {
      case "bar": return (
        <BarForm uniqueCategories={this.props.uniqueCategories} 
                 onChange={this.handleChartSpecificChange}/>);

      default: return <div> Not bar </div>
    }
  }

  // render method for the form
  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <label>
          Visualization type: <br />
          <select value={this.state.chart_type} 
                  name="chart_type" 
                  onChange={this.handleChange}>
            <option value="bar">Bar chart</option>
            <option value="line">Line graph</option>
            <option value="donut">Pie chart</option>
            <option value="boxPlot">Box plot</option>
          </select>
        </label>
        <br />
        {this.renderChartOptions(this.state.chart_type)}
        <br />       
        <label>
          show legend
          <input type="checkbox" 
                 name="legend_on" 
                 checked={this.state.legend_on} 
                 onChange={this.handleChange}/>
        </label>
        <br />
        <label>
          show labels
          <input type="checkbox" 
                 name="labels_on" 
                 checked={this.state.labels_on} 
                 onChange={this.handleChange}/>
        </label>
        <br />
        <input type="submit" value="Submit" />
      </form>
    );
  }
}

export default VisualizationForm;