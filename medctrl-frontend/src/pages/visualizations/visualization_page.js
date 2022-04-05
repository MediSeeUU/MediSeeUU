import React, { Component } from 'react'
import Row from 'react-bootstrap/Row'
import Container from 'react-bootstrap/Container'
import 'bootstrap/dist/css/bootstrap.min.css'

import SingleVisualization from './single_visualization'

// the component that contains all the visualizations
class VisualizationPage extends Component {
  constructor(props) {
    super(props)

    // getting the data
    const data = require('./data.json')

    /* 
      The items array consists of the id's of the visualizations,
		  that are currently in use
		*/
    this.state = { amountOfVisualizations: 0, items: [], data: data }

    // event handlers
    this.handleAddition = this.handleAddition.bind(this)
    this.handleRemoval = this.handleRemoval.bind(this)
  }

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

  //	removes the chosen visualization
  handleRemoval(event) {
    const element = event.target.value
    const currentItems = this.state.items.filter(
      (item) => String(item) !== element
    )
    this.setState({ items: currentItems })
  }

  /*
	  Renders the visualizations.
		The id (element) is used as the key, 
		so React knows which visualizations to show.

		The button for the removal is also here,
		as the logic that keeps track of all the visualization is also here.
	*/
  render() {
    const displayItems = this.state.items.map((element) => {
      return (
        <Row key={element}>
          <SingleVisualization
            number={element}
            data={JSON.parse(JSON.stringify(this.state.data))}
          />
          <button
            id={"deleteButton" + element}
            className="table-buttons button-remove hidden-illegal"
            onClick={this.handleRemoval}
            value={element}
          >
            &#128465;
          </button>
        </Row>
      )
    })

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
  }
}

export default VisualizationPage
