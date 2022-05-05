// external imports
import React, { useEffect, useState } from 'react'
import Row from 'react-bootstrap/Row'
import Container from 'react-bootstrap/Container'
import 'bootstrap/dist/css/bootstrap.min.css'
import ReactModal from 'react-modal'
import SelectedData from '../data/dataComponents/SelectedData'

// internal imports
import SingleVisualization from './single_visualization/SingleVisualization'
import { useSelectedData } from '../../shared/contexts/DataContext'
import GetUniqueCategories from './single_visualization/utils/GetUniqueCategories'
import GenerateBarSeries from './single_visualization/data_interfaces/BarInterface'
import { useVisuals, useVisualsUpdate } from '../../shared/contexts/DataContext'
import { generateSeries } from './single_visualization/SingleVisualization'

// the component that contains all the visualizations
function VisualizationPage() {
  const selectedData = useSelectedData()
  const [tableData, setTableData] = useState(selectedData)
  const [numbers, setNumbers] = useState([])
  const [modal, setModal] = useState(false)

  // event handlers
  const handleAddition = handleAdditionFunc.bind(this)
  const handleRemoval = handleRemovalFunc.bind(this)
  const handleChange = handleChangeFunc.bind(this)
  const handleDataClick = handleDataClickFunc.bind(this)

  //get the visualisation contexts
  var visuals = useVisuals()
  const setVisuals = useVisualsUpdate()

  //get the unique categories for the selected data
  const uniqueCategories =
    selectedData.length > 0 ? GetUniqueCategories(selectedData) : []

  //add some series logic so the controls update
  var updateVisuals = false
  if (visuals.length > 0 && !arrayEquals(visuals[0].data, selectedData)) {
    visuals = visuals.map((vis) => {
      vis.data = selectedData
      vis.uniqueCategories = uniqueCategories
      vis.series = generateSeries(vis.chart_type, vis)
      return vis
    })
    updateVisuals = true
  }

  //update visuals after page render, otherwise react can't handle the calls
  useEffect(() => {
    if (updateVisuals) {
      setVisuals(visuals)
    }
  }, [updateVisuals, visuals, setVisuals])

  //check if two arrays are equal, need to be in the same order
  function arrayEquals(a, b) {
    return (
      Array.isArray(a) &&
      Array.isArray(b) &&
      a.length === b.length &&
      a.every((val, index) => val === b[index])
    )
  }

  // EVENT HANDLERS:

  /* 
	  Adds a new visualization to the array of visualizations.
    The newAmount will serve as the id of the added visualization.
	*/
  function handleAdditionFunc() {
    const newVisual = {
      id: visuals.length + 1,
      chart_type: 'bar',
      chartSpecificOptions: {
        xAxis: 'DecisionYear',
        yAxis: 'Rapporteur',
        categoriesSelected: [],
      },
      legend_on: false,
      labels_on: false,
      data: selectedData,
      series: GenerateBarSeries(
        {
          chartSpecificOptions: {
            xAxis: 'DecisionYear',
            yAxis: 'Rapporteur',
            categoriesSelected: [],
          },
        },
        uniqueCategories,
        selectedData
      ),
      uniqueCategories: uniqueCategories,
      changeName: '',
    }

    const newVisuals = [...visuals, newVisual]
    setVisuals(newVisuals)
  }

  // removes the chosen visualization
  function handleRemovalFunc(id) {
    const currentItems = visuals.filter((item) => item.id !== id)
    setVisuals(currentItems)
  }

  function handleChangeFunc(settings) {
    var newVisuals = JSON.parse(JSON.stringify(visuals))
    newVisuals = newVisuals.map((item) => {
      if (item.id === settings.id) {
        return settings
      }
      return item
    })
    setVisuals(newVisuals)
  }

  // handler that updates the eu_numbers in the table
  /*function handleDataClickFunc(event, chartContext, config) {
    //console.log(config.dataPointIndex)
    //console.log(config.w.config.series[config.seriesIndex].eu_numbers[config.dataPointIndex])
    let eu_numbers = config.w.config.metaData[config.dataPointIndex]
    setNumbers(eu_numbers)
    setModal(true)
  }*/

  function handleDataClickFunc(eu_numbers) {
    setNumbers(eu_numbers)
    if (eu_numbers.length > 0) {
      setModal(true)
    }
  }

  useEffect(() => {
    let updatedData = selectedData.filter((element) => numbers.includes(element.EUNoShort))
    if (updatedData.length <= 0) {
      setModal(false)
    }
    setTableData(updatedData)
  }, [selectedData, numbers])

  // GENERAL FUNCTIONS:

  // Creates the visualizations,
  // gives them a new copy of the data.
  // This should be changed once a context for the data has been implemented
  // As the visualizations should not change the data, only read from it
  function createVisualizations() {
    return visuals.map((visual) => {
      return (
        <Row key={visual.id}>
          <SingleVisualization
            id={visual.id}
            data={tableData}
            settings={visual}
            onRemoval={handleRemoval}
            onFormChangeFunc={handleChange}
            onDataClick={handleDataClick}
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
  if (selectedData?.length > 0) {
    const displayItems = createVisualizations()

    return (
      <div>
        <ReactModal className="visualize-modal" isOpen={modal} onRequestClose={() => setModal(false)} ariaHideApp={false} style={{
            modal: {},
            overlay: {
              background: 'rgba(0, 0, 0, 0.2)',
              backdropFilter: 'blur(2px)',
            },
          }}>
          <i class='bx bx-x close-icon' onClick={() => setModal(false)}></i>
          <SelectedData selectedData={tableData} />
        </ReactModal>
        <Container>
          {displayItems}
          <Row>
            <button
              className="med-primary-solid med-bx-button button-add"
              onClick={handleAddition}
            >
              <i className="bx bx-plus filter-Icon" />
              Add visualization
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

export default VisualizationPage
