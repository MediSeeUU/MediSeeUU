import React from 'react'
import ReactDOM from 'react-dom'
import { render, fireEvent } from '@testing-library/react'
import Table from '../table'
import DummyData from '../../../json/data.json' // we can replace this with a mock API?

test('renders without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <Table data={DummyData} currentPage={1} amountPerPage={10} />,
    root
  )
})

test('at least one column in the table', () => {
  const view = render(
    <Table data={DummyData} currentPage={1} amountPerPage={10} />
  )
  const table = view.getByRole('table')
  const heads = table.getElementsByTagName('thead')
  expect(heads).toHaveLength(1)
  const head = heads[0]
  expect(head.childElementCount).toBeGreaterThan(0)
})

test('at least one row in the table', () => {
  const view = render(
    <Table data={DummyData} currentPage={1} amountPerPage={10} />
  )
  const table = view.getByRole('table')
  const bodies = table.getElementsByTagName('tbody')
  expect(bodies).toHaveLength(1)
  const body = bodies[0]
  expect(body.childElementCount).toBeGreaterThan(0)
})

// test('checkboxes displayed', () => {
//   const data = DummyData
//   const view = render(
//     <Table
//       data={data}
//       selectTable={true}
//       setCheckedState={() => {}}
//       checkedState={Array(data.length).fill(false)}
//       currentPage={1}
//       amountPerPage={10}
//     />
//   )
//   const table = view.getByRole('table')
//   const checkboxes = table.getElementsByClassName('checkboxColumn')
//   expect(checkboxes).toHaveLength(11)
// })

// test('row selected, when checkbox clicked', () => {
//   const data = DummyData
//   let checkedState = Object.assign(
//     {},
//     ...data.map((entry) => ({ [entry.EUNumber]: false }))
//   )
//   const setCheckedState = (newState) => {
//     checkedState = newState
//   }

//   const view = render(
//     <Table
//       data={data}
//       selectTable={true}
//       setCheckedState={setCheckedState}
//       checkedState={checkedState}
//       currentPage={2}
//       amountPerPage={10}
//     />
//   )
//   const table = view.getByRole('table')
//   const checkboxes = table.getElementsByClassName('checkboxColumn')
//   const input = checkboxes[1].getElementsByTagName('input')[0]
//   fireEvent.click(input)
//   expect(checkedState[data[10].EUNumber]).toBe(true)
// })

test('all rows selected when select all pressed', () => {
  const data = DummyData
  let checkedState = Object.assign(
    {},
    ...data.map((entry) => ({ [entry.EUNumber]: false }))
  )
  const setCheckedState = (newState) => {
    checkedState = newState
  }

  const view = render(
    <Table
      data={data}
      selectTable={true}
      setCheckedState={setCheckedState}
      checkedState={checkedState}
      currentPage={2}
      amountPerPage={10}
    />
  )
  const table = view.getByRole('table')
  const checkboxes = table.getElementsByClassName('checkboxColumn')
  const input = checkboxes[0].getElementsByTagName('input')[0]
  fireEvent.click(input)
  let checkedCount = () => {
    let count = 0
    for (const prop in checkedState) {
      if (checkedState[prop]) {
        count++
      }
    }
    return count
  }
  expect(checkedCount()).toBe(data.length)
})

test('throw error when checkedstate not defined and selectTable true', () => {
  const renderFunction = () =>
    render(
      <Table
        data={DummyData}
        selectTable={true}
        setCheckedState={() => {}}
        currentPage={5}
        amountPerPage={10}
      />
    )
  expect(renderFunction).toThrow(Error)
})

test('throw error when setCheckedState not defined and selectable', () => {
  const renderFunction = () =>
    render(
      <Table
        data={DummyData}
        selectTable={true}
        checkedState={[]}
        currentPage={5}
        amountPerPage={10}
      />
    )
  expect(renderFunction).toThrow(Error)
})

test('throw error when data not defined', () => {
  const renderFunction = () =>
    render(
      <Table
        dataToParent={() => {}}
        selectTable={true}
        currentPage={1}
        amountPerPage={10}
      />
    )
  expect(renderFunction).toThrow(Error)
})

test('throw error when currentPage not defined', () => {
  const renderFunction = () =>
    render(
      <Table
        Table
        data={DummyData}
        dataToParent={() => {}}
        selectTable={true}
        amountPerPage={10}
      />
    )
  expect(renderFunction).toThrow(Error)
})

test('throw error when amountPerPage not defined', () => {
  const renderFunction = () =>
    render(
      <Table
        Table
        data={DummyData}
        dataToParent={() => {}}
        currentPage={5}
        selectTable={true}
      />
    )
  expect(renderFunction).toThrow(Error)
})

test('throw error when current page does not exist', () => {
  const renderFunction = () =>
    render(
      <Table
        Table
        data={DummyData}
        dataToParent={() => {}}
        currentPage={5000}
        amountPerPage={100}
        selectTable={true}
      />
    )
  expect(renderFunction).toThrow(Error)
})
