// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

// external imports
import React, { useState } from 'react'
import Row from 'react-bootstrap/Row'
import Container from 'react-bootstrap/Container'
import SelectedData from '../data/selected_data/SelectedData'
import { v4 as uuidv4 } from 'uuid'

// internal imports
import SingleVisualization from './single_visualization/SingleVisualization'
import getUniqueCategories from './single_visualization/utils/getUniqueCategories'
import MedModal from '../../shared/MedModal'
import { useVisuals } from '../../shared/contexts/VisualsContext'
import { useSelectedData } from '../../shared/contexts/SelectedContext'

// the component that contains all the visualizations
function VisualizationPage() {
  // get selected data context and determine unique categories of each variable
  const selectedData = useSelectedData()
  const uniqueCategories =
    selectedData.length > 0 ? getUniqueCategories(selectedData) : []

  // Set popup data.
  // The popup appears when a category of a chart is clicked,
  // e.g. a slice of a pie chart.
  const [popup, setPopup] = useState([])

  // event handlers
  const handleAddition = handleAdditionFunc.bind(this)
  const handleRemoval = handleRemovalFunc.bind(this)
  const handleChange = handleChangeFunc.bind(this)

  // get the visualisation contexts
  const { visuals, setVisuals } = useVisuals()

  // EVENT HANDLERS:

  // adds a new visualization to the visualizations context
  function handleAdditionFunc() {
    const newVisual = {
      id: uuidv4(),
      chartType: 'bar',
      chartSpecificOptions: {
        xAxis: 'eu_aut_date',
        yAxis: 'ema_rapp',
        categoriesSelectedY: uniqueCategories['ema_rapp'],
        categoriesSelectedX: uniqueCategories['eu_aut_date'],
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
    var newVisuals = visuals.map((item) => {
      if (item.id === settings.id) {
        // Resetting the id.
        // Needed when a bar chart, with stacked and stack fully turned on,
        // needs to force a rerender with the stack fully option turned off
        // because of a bug in apex charts
        if (settings.chartSpecificOptions.stacked) {
          settings.id = uuidv4()
        } else if (settings.chartSpecificOptions.stackType) {
          settings.chartSpecificOptions.stackType = false
          settings.id = uuidv4()
        }
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
      // Give the visualization its data and categories,
      // as these can change if data points are removed in the pop-up,
      // without actually reloading the entire component.
      visual.data = selectedData
      visual.uniqueCategories = uniqueCategories
      // These are not included in the initialization of the first visualization,
      // due to the data not being available yet, so they are initialized here.
      visual.chartSpecificOptions.categoriesSelectedX =
        visual.chartSpecificOptions.categoriesSelectedX ??
        uniqueCategories['eu_aut_date']
      visual.chartSpecificOptions.categoriesSelectedY =
        visual.chartSpecificOptions.categoriesSelectedY ??
        uniqueCategories['ema_rapp']

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

  // a message to show the user it has selected data points from the data page
  function renderDataSelectedMessage() {
    const dataPointAmount = selectedData.length
    return (
      <Row>
        <div className="med-content-container med-vis-content-container">
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
    const tableData = selectedData.filter((element) =>
      popup.includes(element.eunumber)
    )
    return (
      <div>
        <MedModal
          showModal={tableData.length > 0}
          closeModal={() => setPopup([])}
          className="med-vis-interactive-data-modal"
        >
          <i
            className="bx bx-x med-close-modal-icon"
            onClick={() => setPopup([])}
          />
          <SelectedData selectedData={tableData} />
        </MedModal>
        <Container>
          {displayDataSelectedMessage}
          {displayItems}
          <Row>
            <button
              className="med-primary-solid med-bx-button med-button-add-vis"
              onClick={handleAddition}
            >
              <i className="bx bx-plus med-button-image" />
              Add visualization
            </button>
          </Row>
        </Container>
      </div>
    )
  } else {
    return (
      <h1 className="med-vis-no-data">
        go to the data page to select datapoints to display
      </h1>
    )
  }
}

export default VisualizationPage
