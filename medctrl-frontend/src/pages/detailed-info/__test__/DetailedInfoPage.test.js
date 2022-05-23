import React from 'react'
import ReactDOM from 'react-dom'
import { fireEvent, render, screen } from '@testing-library/react'
import DetailedInfoPage, { InfoPage } from '../DetailedInfoPage'
import { act } from 'react-dom/test-utils'
import MockDataProvider from '../../../shared/contexts/MockDataContext'
import structData from '../../../shared/contexts/structServer.json'
import { StructureContext } from '../../../shared/contexts/DataContext'
import DummyData from '../detailed-info-data.json'

// https://stackoverflow.com/questions/58117890/how-to-test-components-using-new-react-router-hooks
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'), // use actual for all non-hook parts
  useParams: () => ({
    medID: '1528',
  }),
}))

test('detailed info page renders without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <MockDataProvider>
      <DetailedInfoPage />
    </MockDataProvider>,
    root
  )
})

test('detailed info page displays correct med and proc data', async () => {
  render(
    <MockDataProvider>
      <StructureContext.Provider value={structData}>
        <DetailedInfoPage />
      </StructureContext.Provider>
    </MockDataProvider>
  )

  // wait for the procedure data to be retrieved from the server
  await act(() => new Promise((resolve) => setTimeout(resolve, 1500)))

  const medName = screen.getByText('Comirnaty')
  expect(medName).toBeTruthy()

  const procHeader = screen.getByText('Medicine Timeline')
  expect(procHeader).toBeTruthy()
})

test('detailed info page correctly retrieves medID from url', () => {
  render(
    <MockDataProvider>
      <StructureContext.Provider value={structData}>
        <DetailedInfoPage />
      </StructureContext.Provider>
    </MockDataProvider>
  )

  const medName = screen.getByText('Comirnaty')
  expect(medName).toBeTruthy()
})

test('detailed info page shows error for unknown medIDs', () => {
  render(
    <MockDataProvider>
      <InfoPage medData={null} procData={null} />
    </MockDataProvider>
  )
  const errorMessage = screen.getAllByText('Unknown Medicine ID Number')
  expect(errorMessage).toBeTruthy()
})

test('detailed info page proc select dialog behaves correctly', () => {
  let medData = DummyData.info
  let procData = DummyData.procedures

  render(
    <MockDataProvider>
      <InfoPage medData={medData} procData={procData} />
    </MockDataProvider>
  )

  const procSelectButton = screen.getAllByText('Select Procedures')[0]
  fireEvent.click(procSelectButton)

  const applyButton = screen.getByText('Apply')
  fireEvent.click(applyButton)
})
