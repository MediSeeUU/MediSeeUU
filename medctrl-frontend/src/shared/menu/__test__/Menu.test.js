import React from 'react'
import ReactDOM from 'react-dom'
import {
  render,
  fireEvent,
  waitFor,
  screen,
  cleanup,
  within,
} from '@testing-library/react'
import Menu from '../Menu'
import DummyData from '../../../json/data.json'

test('renders without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(<Menu cachedData={DummyData} />, root)
})

test('opens menu after clicking button', () => {
  render(<Menu cachedData={DummyData} />)
  expect(screen.queryByLabelText(/Menu/i)).not.toBeInTheDocument()
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  expect(screen.getByLabelText(/Menu/i)).toBeInTheDocument()
})

test('apply button calls update function', () => {
  const update = jest.fn()
  render(<Menu cachedData={DummyData} updateTable={update} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  expect(update).not.toHaveBeenCalled()
  fireEvent.click(screen.getByText(/Apply/i))
  expect(update).toHaveBeenCalled()
})

test('clear button calls update function', () => {
  const update = jest.fn()
  render(<Menu cachedData={DummyData} updateTable={update} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  expect(update).not.toHaveBeenCalled()
  fireEvent.click(screen.getByText(/Clear/i))
  expect(update).toHaveBeenCalled()
})

test('clear button resets data', () => {
  const update = (data) => expect(data).toBe(DummyData)
  render(<Menu cachedData={DummyData} updateTable={update} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  fireEvent.click(screen.getByText(/Clear/i))
})

test('close button closes menu', () => {
  render(<Menu cachedData={DummyData} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  fireEvent.click(screen.getByText(/Close/i))
  expect(screen.queryByLabelText(/Menu/i)).not.toBeInTheDocument()
})

test('add filter adds filter item', () => {
  render(<Menu cachedData={DummyData} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  expect(screen.queryAllByRole('combobox')).toHaveLength(1)
  fireEvent.click(screen.getByText(/Add Filter/i))
  expect(screen.queryAllByRole('combobox')).toHaveLength(2)
})

test('single filter applied correctly', () => {
  const update = (data) => {
    data.forEach((element) => {
      expect(element.ApplicationNo.toString()).toContain('8')
    })
  }
  render(<Menu cachedData={DummyData} updateTable={update} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  const select = screen.getByRole('combobox')
  fireEvent.change(select, { target: { value: 'ApplicationNo' } })
  const textBox = screen.getByRole('textbox')
  fireEvent.change(textBox, { target: { value: '8' } })
  fireEvent.focusOut(textBox)
  fireEvent.click(screen.getByText(/Apply/i))
})

test('two filters applied correctly', () => {
  const update = (data) => {
    data.forEach((element) => {
      expect(element.ApplicationNo.toString()).toContain('7')
      expect(element.DecisionYear.toString()).toContain('2001')
    })
  }
  render(<Menu cachedData={DummyData} updateTable={update} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  const firstSelect = screen.getByRole('combobox')
  fireEvent.change(firstSelect, { target: { value: 'ApplicationNo' } })
  const firstText = screen.getByRole('textbox')
  fireEvent.change(firstText, { target: { value: '7' } })
  fireEvent.focusOut(firstText)
  fireEvent.click(screen.getByText(/Add Filter/i))
  const secondSelect = screen.getAllByRole('combobox')[1]
  fireEvent.change(secondSelect, { target: { value: 'DecisionYear' } })
  const secondText = screen.getAllByRole('textbox')[1]
  fireEvent.change(secondText, { target: { value: '2001' } })
  fireEvent.focusOut(secondText)
  fireEvent.click(screen.getByText(/Apply/i))
})

test('multiple values in filter applied correctly', () => {
  const update = (data) => {
    data.forEach((element) => {
      expect(element.DecisionYear.toString()).toMatch(/(1997|2001)/i)
    })
  }
  render(<Menu cachedData={DummyData} updateTable={update} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  const firstSelect = screen.getByRole('combobox')
  fireEvent.change(firstSelect, { target: { value: 'DecisionYear' } })
  const firstText = screen.getByRole('textbox')
  fireEvent.change(firstText, { target: { value: '1997' } })
  fireEvent.focusOut(firstText)
  fireEvent.click(screen.getByText('+ Add'))
  const secondText = screen.getAllByRole('textbox')[1]
  fireEvent.change(secondText, { target: { value: '2001' } })
  fireEvent.focusOut(secondText)
  fireEvent.click(screen.getByText(/Apply/i))
})

test('saved filters in state', () => {
  render(<Menu cachedData={DummyData} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  const select = screen.getByRole('combobox')
  fireEvent.change(select, { target: { value: 'ApplicationNo' } })
  const text = screen.getByRole('textbox')
  fireEvent.change(text, { target: { value: '10' } })
  fireEvent.click(screen.getByText(/Close/i))
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  expect(select.value).toBe('ApplicationNo')
  expect(text.value).toBe('10')
})
