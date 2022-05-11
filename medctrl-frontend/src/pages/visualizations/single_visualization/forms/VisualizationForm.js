import React, { Component } from 'react'
import 'bootstrap/dist/css/bootstrap.min.css'
import { v4 as uuidv4 } from 'uuid'

import BarForm from './types/BarForm'
import LineForm from './types/LineForm'
import PieForm from './types/PieForm'
import HistogramForm from './types/HistogramForm'

// form component for a single visualization
class VisualizationForm extends Component {
  constructor(props) {
    // Recieves the settings, the unique categories and
    // an event handler for changes.
    super(props)

    // initializing the state
    this.state = {
      chartType: this.props.settings.chartType,
      legendOn: this.props.settings.legendOn,
      labelsOn: this.props.settings.labelsOn,
      chartSpecificOptions: this.props.settings.chartSpecificOptions,
      chartSpecificOptionsName: this.props.settings.chartSpecificOptionsName,
    }

    // event handlers
    this.handleChange = this.handleChange.bind(this)
    this.handleChartSpecificChange = this.handleChartSpecificChange.bind(this)
  }

  // EVENT HANDLERS:

  // Event handler for updating the state after a single selection.
  // Do note that if the chart type changes,
  // we still remember the previous options.
  handleChange(event) {
    const target = event.target
    const value = target.type === 'checkbox' ? target.checked : target.value
    const name = target.name

    this.setState(
      {
        [name]: value,
        chartSpecificOptionsName: target.value,
      },
      () => {
        this.props.onChange(this.state)
      }
    )
  }

  // Event handler for updating the state,
  // after the chart specific options were altered.
  // Also updates which value was last updated.
  handleChartSpecificChange(options) {
    this.setState(
      {
        chartSpecificOptions: options[0],
        chartSpecificOptionsName: options[1],
      },
      () => {
        this.props.onChange(this.state)
      }
    )
  }

  // GENERAL FUNCTIONS

  // renders the form for the chosen chart
  renderChartOptions(chartType) {
    switch (chartType) {
      case 'bar':
        return (
          <BarForm
            uniqueCategories={this.props.uniqueCategories}
            onChange={this.handleChartSpecificChange}
            chartSpecificOptions={this.state.chartSpecificOptions}
          />
        )

      case 'line':
        return (
          <LineForm
            uniqueCategories={this.props.uniqueCategories}
            onChange={this.handleChartSpecificChange}
            chartSpecificOptions={this.state.chartSpecificOptions}
          />
        )

      case 'pie':
        return (
          <PieForm
            uniqueCategories={this.props.uniqueCategories}
            onChange={this.handleChartSpecificChange}
            chartSpecificOptions={this.state.chartSpecificOptions}
          />
        )

      case 'histogram':
        return (
          <HistogramForm
            uniqueCategories={this.props.uniqueCategories}
            onChange={this.handleChartSpecificChange}
            chartSpecificOptions={this.state.chartSpecificOptions}
          />
        )

      default:
        throw Error(
          'form error: graph type is ineligible: {' + this.state + '}'
        )
    }
  }

  // RENDERER

  // render method for the form
  render() {
    return (
      <div className="med_visualization_form">
        <label className="visualization-panel-label">
          Visualization type
          <select
            value={this.state.chartType}
            name="chartType"
            className="med-select"
            onChange={this.handleChange}
          >
            <option value="bar">Bar chart</option>
            <option value="line">Line chart</option>
            <option value="pie">Pie chart</option>
            <option value="histogram">Histogram</option>
          </select>
        </label>
        {this.renderChartOptions(this.state.chartType)}
        <label className="visualization-panel-label">
          <input
            type="checkbox"
            name="legendOn"
            checked={this.state.legendOn}
            onChange={this.handleChange}
            value={uuidv4()}
          />
          &nbsp;&nbsp;Show legend
        </label>
        <label className="visualization-panel-label">
          <input
            type="checkbox"
            name="labelsOn"
            checked={this.state.labelsOn}
            onChange={this.handleChange}
            value={uuidv4()}
          />
          &nbsp;&nbsp;Show labels
        </label>
      </div>
    )
  }
}

export default VisualizationForm
