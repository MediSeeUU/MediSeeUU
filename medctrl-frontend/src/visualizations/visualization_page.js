import React, { Component } from "react";
import Row from 'react-bootstrap/Row'
import Container from 'react-bootstrap/Container';
import 'bootstrap/dist/css/bootstrap.min.css';

import SingleVisualization from "./single_visualization";

// the component that contains all the visualizations
class VisualizationPage extends Component {
	constructor(props) {
		super(props);
		/* 
      the items array consists of the id's of the visualizations
		  that are currently in use
		*/
		this.state = {amountOfVisualizations: 0, items: []}

		// event handlers
		this.handleAddition = this.handleAddition.bind(this);
		this.handleRemoval = this.handleRemoval.bind(this);
	}

	/* 
	  adds a new visualization to the array of visualizations
    the newAmount will serve as the id of the added visualization
	*/
	handleAddition(event) {
		const newAmount = this.state.amountOfVisualizations + 1;
		const currentItems = this.state.items;
		this.setState({amountOfVisualizations: newAmount, 
									 items: [...currentItems, newAmount]});
	}

	//	removes the chosen visualization
	handleRemoval(event) {
		const element = event.target.value;
		const currentItems = this.state.items.filter((item) => 
													String(item) !== element);
		this.setState({items: currentItems});
	}


	/*
	  renders the visualizations
		the id (element) is used as the key, 
		so React knows which visualizations to show

		the button for the removal is also here,
		as the logic that keeps track of all the visualizatoin is also here
	*/
	render() {
		const displayItems = this.state.items.map((element) => {
			return (<Row key={element} style={{ marginBottom: '50px'}}>
					      <SingleVisualization number={element}/>
					      <br />
					      <button value = {element} onClick={this.handleRemoval}>
				    		Remove visualization
					      </button>
			       	</Row>);
		});

		return (			
			<div>
				<Container>
					{displayItems}
					<Row>
						<button onClick={this.handleAddition}>
							Add visualization
						</button>
					</Row>
				</Container>
			</div>
		);
	}
}

export default VisualizationPage