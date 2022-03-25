import React, { Component } from "react";
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row'
import Container from 'react-bootstrap/Container';
import 'bootstrap/dist/css/bootstrap.min.css';
import {changeDpiDataUrl} from "changedpi";
import Exports from "apexcharts/src/modules/Exports";
import ApexCharts from "apexcharts";

import VisualizationForm from './visualization_form';
import BarChart from "./visualization_types/bar_chart";
import LineGraph from "./visualization_types/line_graph";
import DonutChart from "./visualization_types/donut_chart";
import BoxPlot from "./visualization_types/box_plot";

// renders the components for a single visualization
class SingleVisualization extends Component {
	constructor(props) {
		super(props);

		let uniqueCategories = this.getUniqueCategories(this.props.data);
		console.log(uniqueCategories);
		let dict = this.pollChosenVariable("DecisionYear", "Rapporteur", uniqueCategories["Rapporteur"])[0];
		let series = this.createSelectedSeries(dict, uniqueCategories["Rapporteur"]);
		//console.log(series);


		this.state = {chart_type: "bar", 
									x_axis: '', 
									y_axis: '',
								  legend_on: true,
								  labels_on: true,
								  data: this.props.data,
								  allUniqueCategories: uniqueCategories,
								  series: series};
		
		// event handlers 
		this.handleChange = this.handleChange.bind(this);
		this.handleExport = this.handleExport.bind(this);
	}

  // event handler for the form data
	handleChange(event) {
    this.setState({chart_type: event.chart_type, 
									 x_axis: event.x_axis, 
									 y_axis: event.y_axis,
									 legend_on: event.legend_on,
									 labels_on: event.labels_on});

		

		let dictAndCats = this.pollChosenVariables("DecisionYear", ["AEC"]);
		let dict = dictAndCats[0];
		let uniqueCategories = dictAndCats[1];
		let newseries = Object.values(this.createSeries(dict, ["AEC"]))[0];

		// actually updating the parameters of the chart
		// we may want to do this purely using the states,
		// but I am not sure how to do that yet
		ApexCharts.getChartByID(this.props.number).updateOptions({
    	dataLabels: {enabled: event.labels_on},
	  	legend: {show: event.legend_on},
			xaxis: {categories: uniqueCategories}
		});

		ApexCharts.getChartByID(this.props.number).updateSeries([{
			data: newseries
		}]);

		
  }

	pollChosenVariable(x_axis, y_axis, categories_y) {
		let dict = {};
		let uniqueCategories = [];
		this.props.data.forEach((element) => {
			if (uniqueCategories.includes(element[x_axis])) {
				if (categories_y.includes(element[y_axis])) {
					if (dict[element[x_axis]][element[y_axis]] === undefined) {
						dict[element[x_axis]][element[y_axis]] = 1;
					}
					else {
						dict[element[x_axis]][element[y_axis]]+= 1;
					}	
				}
			}
			else {				
				if (categories_y.includes(element[y_axis])) {
					dict[element[x_axis]] = {};
					dict[element[x_axis]][element[y_axis]] = 1;
					uniqueCategories = [...uniqueCategories, element[x_axis]];
				}							
			}
		})
		//console.log(dict);
		return [dict, uniqueCategories.sort()];
	}


	pollChosenVariables(x_axis, y_axis) {
		let dict = {};
		let uniqueCategories = [];
		this.props.data.forEach((element) => {
			if (uniqueCategories.includes(element[x_axis])) {
				for (let attribute in element) {
					if (y_axis.includes(attribute)) {
						dict[element[x_axis]][attribute]+= 1;
					}
				}
			}
			else {
				dict[element[x_axis]] = {};
				for (let attribute in element) {
					if (y_axis.includes(attribute)) {					
						dict[element[x_axis]][attribute] = 1;
					}
				}			
				uniqueCategories = [...uniqueCategories, element[x_axis]];
			}
		});
		//console.log(dict);
		return [dict, uniqueCategories.sort()];
	}

	createSelectedSeries(dict, categories_y) {
		let series = {}

		//y_axis.forEach(attribute => {
		//	series[attribute] = [];
		//});

		let keys = Object.keys(dict);
		keys = keys.sort();

		console.log(categories_y);
		keys.forEach((k) => {
			for (let category in categories_y) {
				category = categories_y[category];
				if (series[category] === undefined) {
					series[category] = [];
					if ((category in dict[k])) {
						
						series[category].push(dict[k][category]);
					}		
					else {
						series[category].push(0);
					}			
				}
				else {
					if (!(dict[k][category] === undefined)) {
						series[category].push(dict[k][category]);
					}			
					else {
						series[category].push(0);
					}		
				}			
			}
		})

		//console.log(series);
		return series;
	}

	createSeries(dict, y_axis) {
		let series = {}

		//y_axis.forEach(attribute => {
		//	series[attribute] = [];
		//});

		let keys = Object.keys(dict);
		keys = keys.sort();

		keys.forEach((k) => {
			for (var attribute in dict[k]) {
				series[attribute].push(dict[k][attribute]);
			}
		})

		//console.log(series);
		return series;
	}


	getUniqueCategories(data) {
		let dict = {};

		data.forEach(element => {
			for (let attribute in element) {
				let val = element[attribute];
				if (dict[attribute] === undefined) {
					dict[attribute] = [val];
				}
				else {
					if (!(dict[attribute].includes(val))) {
						dict[attribute].push(val);
					}			 
				}
			}
		});

		//console.log(dict);
		return dict;
	}



  
	/*
	  event handler for exporting the visualization to svg and png
		does not export the actual data
		currently does both the svg and the png export at once,
		seperate buttons should be made!
	*/
	handleExport(event) {
		/* 
		  get the visualization in the base64 format
			we scale it for a better resolution
		*/
		ApexCharts.exec(String(this.props.number), 
										"dataURI", 
										{scale: 3.5}).then(({ imgURI}) => {
			// changes the dpi of the visualization to 300
      const dataURI300 = changeDpiDataUrl(imgURI, 300);
		  let exp = 
				new Exports(ApexCharts.getChartByID(String(this.props.number)));

			// does not currently export it using the title of the visualization,
			// as the title is not currently set as an option for the user to enter
		  exp.triggerDownload(dataURI300, 
				exp.w.config.chart.toolbar.export.png.filename, '.png');
		  exp.exportToSVG(ApexCharts.getChartByID(String(this.props.number)));
    })
	}

	// creating a chart based on the chosen chart type
	chooseChart(chart_type) {
		const legend_on = this.state.legend_on;
		const labels_on = this.state.labels_on;
		
		switch(chart_type) {
			case "bar": return <BarChart legend={legend_on} 
																	 labels={labels_on}
																	 number={this.props.number}
																	 data={this.props.data}
																	 series={this.state.series}
																	 categories={this.state.allUniqueCategories}/>;
			
			case "line": return <LineGraph legend={legend_on} 
																		 labels={labels_on} 
																		 number={this.props.number}/>;
			
			case "donut": return <DonutChart legend={legend_on} 
																			 labels={labels_on} 
																			 number={this.props.number}/>;

			case "boxPlot": return <BoxPlot legend={legend_on} 
																			labels={labels_on} 
																			number={this.props.number}/>;

			default: return <BarChart legend={legend_on} 
																labels={labels_on} 
																number={this.props.number}/>;									
		}
	}
 	
  /*
	  renders a single visualization
		based on the layout from the prototype:
		divides the visualization in a left part for the form,
		a right-lower part for the visualization and 
		a right-upper part for the filters
	*/
	render() {
		return (			
			<div>
				<Container>
					<Row>
						<Col sm={4} style={{backgroundColor: 'grey', 
																borderRadius: '15px', 
																borderRight: '2px solid black'}}>
								<VisualizationForm onFormChange={this.handleChange}/></Col>
					  <Col sm={8}>
							<Row>
								hello
							</Row>
							<Row>
								{this.chooseChart(this.state.chart_type)}
							</Row>
						</Col>	
					</Row>
					<Row>
					  <button onClick={this.handleExport}>
							Print to svg
						</button>	
					</Row>						
				</Container>
			</div>
			
		)
	}
}

export default SingleVisualization;