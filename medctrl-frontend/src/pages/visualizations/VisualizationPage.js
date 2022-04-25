// external imports
import React, { Component } from 'react'
import Row from 'react-bootstrap/Row'
import Container from 'react-bootstrap/Container'
import 'bootstrap/dist/css/bootstrap.min.css'

// internal imports
import SingleVisualization from './single_visualization/SingleVisualization'

// the component that contains all the visualizations
class VisualizationPage extends Component {
  constructor(props) {
    super(props)

    // getting the data
    const data = this.props.selectedData

    /* 
      The items array consists of the id's of the visualizations,
		  that are currently in use.
		*/
    this.state = { amountOfVisualizations: 1, items: [1], data: data }

    // event handlers
    this.handleAddition = this.handleAddition.bind(this)
    this.handleRemoval = this.handleRemoval.bind(this)
  }

  // EVENT HANDLERS:

  /* 
	  Adds a new visualization to the array of visualizations.
    The newAmount will serve as the id of the added visualization.
	*/
  handleAddition(event) {
    const newAmount = this.state.amountOfVisualizations + 1
    const currentItems = this.state.items
    this.setState({
      amountOfVisualizations: newAmount,
      items: [...currentItems, newAmount],
    })
  }

  // removes the chosen visualization
  handleRemoval(id, event) {
    const currentItems = this.state.items.filter((item) => item !== id)
    this.setState({ items: currentItems })
  }

  // GENERAL FUNCTIONS:

  // Creates the visualizations,
  // gives them a new copy of the data.
  // This should be changed once a context for the data has been implemented
  // As the visualizations should not change the data, only read from it
  createVisualizations() {
    return this.state.items.map((id) => {
      return (
        <Row key={id}>
          <SingleVisualization
            id={id}
            data={this.state.data}
            onRemoval={this.handleRemoval}
          />
        </Row>
      )
    })
  }

  // RENDERER:

  /*
	  Renders the visualizations.
		The id is used as the key, 
		so React knows which visualizations to show.
	*/
  render() {
    if (this.props.selectedData?.length > 0) {
      const displayItems = this.createVisualizations()

      return (
        <div>
          <Container>
            {displayItems}
            <Row>
              <button
                className="table-buttons button-add"
                onClick={this.handleAddition}
              >
                <i className="bx bx-plus filter-Icon"></i>Add visualization
              </button>
            </Row>
          </Container>
        </div>
      )
    } else {
      return (
        <h1 className="visualization-no-data">No data selected to display</h1>
      )
    }
  }
}

export default VisualizationPage
