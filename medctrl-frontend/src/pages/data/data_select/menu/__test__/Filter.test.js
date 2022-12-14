// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'
import ReactDOM from 'react-dom'
import { render, fireEvent, screen } from '@testing-library/react'
import Filter from '../filter_menu/Filter'
import FilterInputs from '../filter_menu/FilterInputs'
import MockProvider from '../../../../../mocks/MockProvider'

test('renders without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <Filter item={{ selected: 'BrandName', input: [''] }} />,
    root
  )
})

test('delete filter function is called', () => {
  const del = jest.fn()
  render(
    <Filter id={10} item={{ selected: 'BrandName', input: [''] }} del={del} />
  )
  fireEvent.click(screen.getByTestId('delete-icon'))
  expect(del).toHaveBeenCalled()
})

test('delete filter returns correct id', () => {
  const del = (id) => {
    expect(id).toBe(10)
  }
  render(
    <Filter id={10} item={{ selected: 'BrandName', input: [''] }} del={del} />
  )
  fireEvent.click(screen.getByTestId('delete-icon'))
})

test('add filter box function is called', () => {
  const box = jest.fn()
  render(
    <Filter id={10} item={{ selected: 'BrandName', input: [''] }} box={box} />
  )
  fireEvent.click(screen.getByTestId('add-label'))
  expect(box).toHaveBeenCalled()
})

test('add filter box returns correct id', () => {
  const box = (id) => {
    expect(id).toBe(7)
  }
  render(
    <Filter id={7} item={{ selected: 'BrandName', input: [''] }} box={box} />
  )
  fireEvent.click(screen.getByTestId('add-label'))
})

test('delete filter box function is called', () => {
  const dbox = jest.fn()
  render(
    <Filter id={10} item={{ selected: 'BrandName', input: [''] }} dbox={dbox} />
  )
  fireEvent.click(screen.getByTestId('remove-icon'))
  expect(dbox).toHaveBeenCalled()
})

test('delete filter box returns correct ids', () => {
  const dbox = (id, bid) => {
    expect(id).toBe(4)
    expect(bid).toBe(2)
  }
  render(
    <Filter
      id={4}
      item={{
        selected: 'BrandName',
        input: ['hi', 'there', 'this needs to be removed', 'this not'],
      }}
      dbox={dbox}
    />
  )
  const removes = screen.getAllByTestId('remove-icon')
  fireEvent.click(removes[2])
})

test('change selected function is called', () => {
  const sel = jest.fn()
  render(
    <Filter id={10} item={{ selected: 'BrandName', input: [''] }} sel={sel} />
  )
  const select = screen.getByTestId('filter-select')
  fireEvent.change(select, { target: { value: 'BrandName' } })
  expect(sel).toHaveBeenCalled()
})

test('change selected returns correct id and value', () => {
  const sel = (id, value) => {
    expect(id).toBe(12)
    expect(value).toBe('BrandName')
  }
  render(
    <MockProvider>
      <Filter
        id={12}
        options={<option value="BrandName">this should not matter</option>}
        item={{ selected: 'BrandName', input: [''] }}
        sel={sel}
      />
    </MockProvider>
  )
  const select = screen.getByTestId('filter-select')
  fireEvent.change(select, { target: { value: 'BrandName' } })
})

test('change input function is called', () => {
  const fil = jest.fn()
  render(
    <Filter
      id={10}
      item={{
        selected: 'Rapporteur',
        input: [{ var: '', filterRange: 'from', custom: true }],
      }}
      fil={fil}
    />
  )
  const input = screen.getByTestId('input-select')
  fireEvent.change(input, { target: { value: 'can be anything' } })
  expect(fil).toHaveBeenCalled()
})

test('change input function returns correct ids and value', () => {
  const categories = {
    Rapporteur: ['Netherlands', 'Belgium', 'Germany'],
  }
  const fil = (id, index, value) => {
    expect(id).toBe(52)
    expect(index).toBe(1)
    expect(value).toBe('Belgium')
  }
  render(
    <Filter
      id={52}
      item={{
        selected: 'Rapporteur',
        input: [
          { var: 'hi', custom: true },
          { var: 'there', custom: true },
          { var: 'again', custom: true },
        ],
      }}
      fil={fil}
      cats={categories}
    />
  )
  const inputs = screen.getAllByTestId('input-select')
  fireEvent.change(inputs[1], { target: { value: 'Belgium' } })
})

test('text filter rendered', () => {
  const root = document.createElement('div')

  ReactDOM.render(
    <FilterInputs
      props={{
        id: '1',
        item: {
          selected: 'BrandName',
          input: [{ var: 'test', filterRange: 'from', custom: true }],
          filterType: 'text',
        },
        options: 'not important',
      }}
      i={'0'}
    />,
    root
  )
})

test('number from filter rendered', () => {
  const root = document.createElement('div')

  ReactDOM.render(
    <FilterInputs
      props={{
        id: '1',
        item: {
          selected: 'null',
          input: [{ var: '20', filterRange: 'from', custom: true }],
          filterType: 'number',
        },
        options: 'not important',
      }}
      i={'0'}
    />,
    root
  )
})

test('number till filter rendered', () => {
  const root = document.createElement('div')

  ReactDOM.render(
    <FilterInputs
      props={{
        id: '1',
        item: {
          selected: null,
          input: [{ var: '20', filterRange: 'till', custom: true }],
          filterType: 'number',
        },
        options: 'not important',
      }}
      i={'0'}
    />,
    root
  )
})

test('date from filter rendered', () => {
  const root = document.createElement('div')

  ReactDOM.render(
    <FilterInputs
      props={{
        id: '1',
        item: {
          selected: null,
          input: [{ var: '2012-02-02', filterRange: 'from', custom: true }],
          filterType: 'date',
        },
        options: 'not important',
      }}
      i={'0'}
    />,
    root
  )
})

test('date till filter rendered', () => {
  const root = document.createElement('div')

  ReactDOM.render(
    <FilterInputs
      props={{
        id: '1',
        item: {
          selected: null,
          input: [{ var: '2012-02-02', filterRange: 'till', custom: true }],
          filterType: 'date',
        },
        options: 'not important',
      }}
      i={'0'}
    />,
    root
  )
})

test('bool filter rendered', () => {
  const root = document.createElement('div')

  ReactDOM.render(
    <FilterInputs
      props={{
        id: '1',
        item: {
          selected: null,
          input: [{ var: 'yes', filterRange: 'from', custom: true }],
          filterType: 'bool',
        },
        options: 'not important',
      }}
      i={'0'}
    />,
    root
  )
})
