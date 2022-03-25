import React, { Component } from "react";
import 'bootstrap/dist/css/bootstrap.min.css';

// form component for a single visualization
class VisualizationForm extends Component {
  constructor(props) {
    super(props);

    this.state = {chart_type: "bar", 
                  x_axis: "test", 
                  y_axis: "test",
                  legend_on: true,
                  labels_on: true};

    // event handlers
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  // event handler for updating the state after a single selection 
  handleChange(event) {
    const target = event.target;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const name = target.name;
    this.setState({[name]: value});
  }

  // event handler for the submission after all selections
  handleSubmit(event) {
    // makes sure that the page does not reload and thus resets the data
    event.preventDefault();
    // function passed down as a prop by SingleVisualization
    this.props.onFormChange(this.state);
  }

  // render method for the form
  // the last 2 drop down menus can be removed
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
        <label>
          Variable: <br />
          <select value={this.state.x_axis} 
                  name="x_axis" 
                  onChange={this.handleChange}>
            <option value="test">test value</option>
          </select>
        </label>
        <br />
        <label>
          Amount of: <br />
          <select value={this.state.y_axis} 
                  name="y_axis" 
                  onChange={this.handleChange}>
            <option value="grapefruit">Grapefruit</option>
            <option value="lime">Lime</option>
            <option value="coconut">Coconut</option>
            <option value="mango">Mango</option>
          </select> 
        </label>
        <br />       
        <label>
          show legend
          <input type="checkbox" 
                 name="legend_on" 
                 checked={this.state.legend_on} 
                 onChange={this.handleChange}/>
        </label>
        <br />
        <label htmlFor="generalOption2">
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