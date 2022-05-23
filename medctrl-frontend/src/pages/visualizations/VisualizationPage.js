// external imports
import React, { useEffect, useState, useRef } from 'react'
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
import { generateSeries } from './single_visualization/utils/GenerateSeries'

// the component that contains all the visualizations
function VisualizationPage() {
  const selectedData = useSelectedData()

  const [tableData, setTableData] = useState([]) // Data displayed in the modal table
  const [numbers, setNumbers] = useState([]) // The eu numbers that correspond to the clicked selection
  const [modal, setModal] = useState(false) // State of modal (open or closed)
  const [keys, setKeys] = useState([''])
  const [series, setSeries] = useState([[]])

  // event handlers
  const handleAddition = handleAdditionFunc.bind(this)
  const handleRemoval = handleRemovalFunc.bind(this)
  const handleChange = handleChangeFunc.bind(this)
  const handleDataClick = handleDataClickFunc.bind(this)

  // get the visualisation contexts
  var visuals = useVisuals()
  const setVisuals = useVisualsUpdate()

  // get the unique categories for the selected data
  const uniqueCategories =
    selectedData.length > 0 ? GetUniqueCategories(selectedData) : []

  // add some series logic so the controls update
  // var updateVisuals = false
  // if (
  //   selectedData.length > 0 &&
  //   visuals.length > 0 &&
  //   !arrayEquals(visuals[0].data, selectedData)
  // ) {
  //   visuals = visuals.map((vis) => {
  //     vis.data = selectedData
  //     vis.uniqueCategories = uniqueCategories
  //     let newSeries = generateSeries(vis.chartType, vis)
  //     if (JSON.stringify(vis.series) !== JSON.stringify(newSeries)) {
  //       console.log("updating all keys")
  //       series[vis.id] = newSeries
  //       setSeries(series)
  //       keys[vis.id] = uuidv4()
  //       setKeys(keys)
  //     }
  //     return vis
  //   })
  //   updateVisuals = true
  // }

  // // update visuals after page render, otherwise react can't handle the calls
  // useEffect(() => {
  //   if (updateVisuals) {
  //     setVisuals(visuals)
  //   }
  // }, [updateVisuals, visuals, setVisuals])

  // // check if two arrays are equal, need to be in the same order
  // function arrayEquals(a, b) {
  //   return (
  //     Array.isArray(a) &&
  //     Array.isArray(b) &&
  //     a.length === b.length &&
  //     a.every((val, index) => val === b[index])
  //   )
  // }

  // Keep a reference of the selected data and update series if it changed
  const dataRef = useRef([])
  if (JSON.stringify(dataRef.current) !== JSON.stringify(selectedData)) {
    dataRef.current = selectedData
    let newVisuals = visuals.map((vis) => {
      vis.data = selectedData
      vis.uniqueCategories = uniqueCategories
      vis.chartSpecificOptions.categoriesSelectedX =
        uniqueCategories[vis.chartSpecificOptions.xAxis]
      vis.chartSpecificOptions.categoriesSelectedY =
        uniqueCategories[vis.chartSpecificOptions.yAxis]
      let newSeries = generateSeries(vis.chartType, vis)
      series[vis.id] = newSeries
      setSeries(series)
      keys[vis.id] = uuidv4()
      setKeys(keys)
      return vis
    })
    setVisuals(newVisuals)
  }

  // EVENT HANDLERS:

  // adds a new visualization to the visualizations context
  function handleAdditionFunc() {
    const newVisual = {
      id: visuals.length,
      chartType: 'bar',
      chartSpecificOptions: {
        xAxis: 'DecisionYear',
        yAxis: 'Rapporteur',
        categoriesSelectedY: uniqueCategories['Rapporteur'],
        categoriesSelectedX: uniqueCategories['DecisionYear'],
      },
      legendOn: false,
      labelsOn: false,
      data: selectedData,
      uniqueCategories: uniqueCategories,
    }

    const newVisuals = [...visuals, newVisual]
    setSeries([...series, generateSeries('bar', newVisual)])
    setKeys([...keys, uuidv4()])
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
        settings.data = selectedData
        settings.uniqueCategories = uniqueCategories
        series[settings.id] = generateSeries(settings.chartType, settings)
        setSeries(series)
        keys[settings.id] = uuidv4()
        setKeys(keys)
        return settings
      }
      return item
    })
    setVisuals(newVisuals)
  }

  // Handler that is called after clicking on a datapoint
  // It will set the eu numbers state to the eu numbers of the selected datapoint
  // And opens the pop-up which displays the entries in the table
  function handleDataClickFunc(numbers) {
    setNumbers(numbers)
    if (numbers.length > 0) {
      setModal(true)
    }
  }

  // Updates the states after changes to the selected data or eu numbers
  // The table data will be all the data with eu numbers that are currently stored in the state
  useEffect(() => {
    if (numbers.length > 0 && modal) {
      let updatedData = selectedData.filter((element) =>
        numbers.includes(element.EUNoShort)
      )
      if (updatedData.length <= 0) {
        setModal(false)
      }
      setTableData(updatedData)
    }
  }, [selectedData, numbers, modal])

  // GENERAL FUNCTIONS:

  // creates the visualizations
  function renderVisualizations() {
    return visuals.map((visual) => {
      return (
        <Row key={visual.id}>
          <SingleVisualization
            id={visual.id}
            data={selectedData}
            settings={visual}
            onRemoval={handleRemoval}
            onFormChangeFunc={handleChange}
            onDataClick={handleDataClick}
            keys={keys}
            series={series}
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
    return (
      <div>
        <ReactModal
          className="visualize-modal"
          isOpen={modal}
          onRequestClose={() => setModal(false)}
          ariaHideApp={false}
          style={{
            modal: {},
            overlay: {
              background: 'rgba(0, 0, 0, 0.2)',
              backdropFilter: 'blur(2px)',
            },
          }}
        >
          <i className="bx bx-x close-icon" onClick={() => setModal(false)}></i>
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
