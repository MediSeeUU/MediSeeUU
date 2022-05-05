import React, { Component } from 'react'
import 'bootstrap/dist/css/bootstrap.min.css'

import BarForm from './types/BarForm'
import LineForm from './types/LineForm'
import PieForm from './types/PieForm'
import HistogramForm from './types/HistogramForm'

// form component for a single visualization
class VisualizationForm extends Component {
  constructor(props) {
    super(props)

    // Initializing the state, options are off to keep the start quick.
    // The chartSpecificOptionsName is used for determining the key of
    // the actual chart, to notify the chart that it has been updated.
    this.state = {
      chart_type: this.props.settings.chart_type,
      legend_on: this.props.settings.legend_on,
      labels_on: this.props.settings.labels_on,
      chartSpecificOptions: this.props.settings.chartSpecificOptions,
      chartSpecificOptionsName: this.props.settings.chartSpecificOptionsName,
    }

    // event handlers
    this.handleChange = this.handleChange.bind(this)
    this.handleChartSpecificChange = this.handleChartSpecificChange.bind(this)
  }

  // EVENT HANDLERS:

  // event handler for updating the state after a single selection
  handleChange(event) {
    const target = event.target
    const value = target.type === 'checkbox' ? target.checked : target.value
    const name = target.name

    //  the chart specific values depend on which chart type has been chosen,
    //  so if the chart type changes, this needs to be re-initialized
    if (name === 'chart_type') {
      //this.resetChartSpecifics(value)
    }
    this.setState({ [name]: value }, () => {
      this.props.onChange(this.state)
    })
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

  // re-initializing the state depending on which new chart type has been chosen
  resetChartSpecifics(chartType) {
    const chartSpecificOptions = this.state.chartSpecificOptions
    switch (chartType) {
      case 'bar': {
        this.setState({
          chartSpecificOptions: {
            yAxis: chartSpecificOptions.yAxis,
            xAxis: 'DecisionYear',
            categoriesSelectedX: this.props.uniqueCategories['DecisionYear'],
            categoriesSelectedY: this.props.uniqueCategories['Rapporteur'],
          },
          chartSpecificOptionsName: '',
        })
        break
      }

      case 'line': {
        this.setState({
          chartSpecificOptions: {
            yAxis: 'Rapporteur',
            xAxis: 'DecisionYear',
            categoriesSelectedX: this.props.uniqueCategories['DecisionYear'],
            categoriesSelectedY: this.props.uniqueCategories['Rapporteur'],
          },
          chartSpecificOptionsName: '',
        })
        break
      }

      case 'pie': {
        this.setState({
          chartSpecificOptions: {
            chosenVariable: 'Rapporteur',
            categoriesSelectedX: this.props.uniqueCategories['Rapporteur'],
          },
          chartSpecificOptionsName: '',
        })
        break
      }

      case 'histogram': {
        this.setState({
          chartSpecificOptions: {
            yAxis: chartSpecificOptions.yAxis,
            chosenVariable: 'Rapporteur',
            categoriesSelectedX: this.props.uniqueCategories['Rapporteur'],
          },
          chartSpecificOptionsName: '',
        })
        break
      }

      default:
        return
    }
  }

  // renders the form for the chosen chart
  renderChartOptions(chart_type) {
    switch (chart_type) {
      case 'bar':
        return (
          <BarForm
            uniqueCategories={this.props.uniqueCategories}
            onChange={this.handleChartSpecificChange}
            graphSettings={this.state.chartSpecificOptions}
          />
        )

      case 'line':
        return (
          <LineForm
            uniqueCategories={this.props.uniqueCategories}
            onChange={this.handleChartSpecificChange}
            graphSettings={this.state.chartSpecificOptions}
          />
        )

      case 'pie':
        return (
          <PieForm
            uniqueCategories={this.props.uniqueCategories}
            onChange={this.handleChartSpecificChange}
            graphSettings={this.state.chartSpecificOptions}
          />
        )

      case 'histogram':
        return (
          <HistogramForm
            uniqueCategories={this.props.uniqueCategories}
            onChange={this.handleChartSpecificChange}
          />
        )

      default:
        return <div> choose a form type </div>
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
            value={this.state.chart_type}
            name="chart_type"
            className="med-select"
            onChange={this.handleChange}
          >
            <option value="bar">Bar chart</option>
            <option value="line">Line chart</option>
            <option value="pie">Pie chart</option>
            <option value="histogram">Histogram</option>
          </select>
        </label>
        {this.renderChartOptions(this.state.chart_type)}
        <label className="visualization-panel-label">
          <input
            type="checkbox"
            name="legend_on"
            checked={this.state.legend_on}
            onChange={this.handleChange}
          />
          &nbsp;&nbsp;Show legend
        </label>
        <label className="visualization-panel-label">
          <input
            type="checkbox"
            name="labels_on"
            checked={this.state.labels_on}
            onChange={this.handleChange}
          />
          &nbsp;&nbsp;Show labels
        </label>
      </div>
    )
  }
}

export default VisualizationForm
