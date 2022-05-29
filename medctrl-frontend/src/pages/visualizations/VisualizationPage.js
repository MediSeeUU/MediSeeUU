// external imports
import React, { useState } from 'react'
import Row from 'react-bootstrap/Row'
import Container from 'react-bootstrap/Container'
import 'bootstrap/dist/css/bootstrap.min.css'
import ReactModal from 'react-modal'
import SelectedData from '../data/dataComponents/SelectedData'
import { v4 as uuidv4 } from 'uuid'

// internal imports
import SingleVisualization from './single_visualization/SingleVisualization'
import { useSelectedData } from '../../shared/contexts/DataContext'
import GetUniqueCategories from './single_visualization/utils/GetUniqueCategories'
import { useVisuals, useVisualsUpdate } from '../../shared/contexts/DataContext'

// the component that contains all the visualizations
function VisualizationPage() {
  // get selected data context and determine unique categories
  const selectedData = useSelectedData()
  const uniqueCategories = selectedData.length > 0 ? GetUniqueCategories(selectedData) : []
  
  // set popup data
  const [popup, setPopup] = useState([])

  // event handlers
  const handleAddition = handleAdditionFunc.bind(this)
  const handleRemoval = handleRemovalFunc.bind(this)
  const handleChange = handleChangeFunc.bind(this)

  // get the visualisation contexts
  var visuals = useVisuals()
  const setVisuals = useVisualsUpdate()

  // adds a new visualization to the visualizations context
  function handleAdditionFunc() {
    const newVisual = {
      id: uuidv4(),
      chartType: 'bar',
      chartSpecificOptions: {
        xAxis: 'DecisionYear',
        yAxis: 'Rapporteur',
        categoriesSelectedY: uniqueCategories['Rapporteur'],
        categoriesSelectedX: uniqueCategories['DecisionYear'],
      },
      legendOn: false,
      labelsOn: false,
    }

    const newVisuals = [...visuals, newVisual]
    setVisuals(newVisuals)
  }

  // removes the chosen visualization
  function handleRemovalFunc(id) {
    const currentItems = visuals.filter((item) => item.id !== id)
    setVisuals(currentItems)
  }

  // handles a change to a visualization
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

  // GENERAL FUNCTIONS:

  // creates the visualizations
  function renderVisualizations() {
    return visuals.map((visual) => {
      visual.data = selectedData
      visual.uniqueCategories = uniqueCategories
      return (
        <Row key={visual.id}>
          <SingleVisualization
            settings={visual}
            onRemoval={handleRemoval}
            onFormChangeFunc={handleChange}
            onDataClick={setPopup}
          />
        </Row>
      )
    })
  }

  // a message to show the user it has selected data points are the data page
  function renderDataSelectedMessage() {
    const dataPointAmount = selectedData.length
    return (
      <Row>
        <div className="med-content-container visual-container">
          <b>
            You have currently selected {dataPointAmount} datapoint(s).
            <br />
            Go to the data page to add/remove datapoint(s).
            <br />
            In case some of the functionality is not clear, you can visit the
            manual on the home page
          </b>
        </div>
      </Row>
    )
  }

  // RENDERER:

  // renders the visualizations
  if (selectedData?.length > 0) {
    const displayItems = renderVisualizations()
    const displayDataSelectedMessage = renderDataSelectedMessage()
    const tableData = selectedData.filter((element) => popup.includes(element.EUNoShort))
    return (
      <div>
        <ReactModal
          className="visualize-modal"
          isOpen={tableData.length > 0}
          onRequestClose={() => setPopup([])}
          ariaHideApp={false}
          style={{
            modal: {},
            overlay: {
              background: 'rgba(0, 0, 0, 0.2)',
              backdropFilter: 'blur(2px)',
            },
          }}
        >
          <i className="bx bx-x close-icon" onClick={() => setPopup([])}></i>
          <SelectedData selectedData={tableData} />
        </ReactModal>
        <Container>
          {displayDataSelectedMessage}
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
      <h1 className="visualization-no-data">
        go to the data page to select datapoints to display
      </h1>
    )
  }
}

export default VisualizationPage
