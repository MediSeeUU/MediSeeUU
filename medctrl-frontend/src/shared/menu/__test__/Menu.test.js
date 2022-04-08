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
import Menu from '../menu'
import DummyData from '../../../json/data.json'
import { convertSortingAttributeNameToComparisonFunction } from '../sorting'

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
  expect(screen.queryAllByTestId('filter-select')).toHaveLength(1)
  fireEvent.click(screen.getByText(/Add Filter/i))
  expect(screen.queryAllByTestId('filter-select')).toHaveLength(2)
})




test('single filter applied correctly', () => {
  const update = (data) => {
    data.forEach((element) => {
      expect(element.ApplicationNo.toString()).toContain('8')
    })
  }
  render(<Menu cachedData={DummyData} updateTable={update} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  const select = screen.queryByTestId('filter-select')
  fireEvent.change(select, { target: { value: 'ApplicationNo' } })
  const textBox = screen.getByRole('textbox')
  fireEvent.change(textBox, { target: { value: '8' } })
  fireEvent.focusOut(textBox)
  fireEvent.click(screen.getByText(/Apply/i))
})
// test for checking if clicking the "Add sorting option" label adds an sorting-item (A)
test('add sorting option adds sorting item', () => {
  render(<Menu cachedData={DummyData} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  expect(screen.queryAllByTestId('sort-select-attr')).toHaveLength(1)
  fireEvent.click(screen.getByText(/Add Sorting option +/i))
  expect(screen.queryAllByTestId('sort-select-attr')).toHaveLength(2)
})
//test to check if single parameter sorting ascending on ApplicationNo (number) works
test('single ascending sorter on ApplicationNo applied correctly', () => {
  const update = (data) => {
    var compareFunc = convertSortingAttributeNameToComparisonFunction("ApplicationNo")
    for(var i=0; i<Object.keys(data).length-1; i++)
    {
      var comparisonvalue = compareFunc(data[i], data[i+1])
      expect(comparisonvalue).toBeLessThanOrEqual(0)
    } 
  }
  render(<Menu cachedData={DummyData} updateTable={update} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  const selectedAttribute = screen.queryByTestId('sort-select-attr')
  fireEvent.change(selectedAttribute, { target: { value: "ApplicationNo" } })
  const selectedOrder = screen.getByTestId('sort-select-order')
  fireEvent.change(selectedOrder, { target: { value: "asc" } })

  // temp neccessarry to change filter state, otherwise no sorting is applied
  const select = screen.queryByTestId('filter-select')
  fireEvent.change(select, { target: { value: 'CMA' } })
  const textBox = screen.getByRole('textbox')
  fireEvent.change(textBox, { target: { value: 'no' } })
  fireEvent.focusOut(textBox)
  //

  fireEvent.click(screen.getByText(/Apply/i))
})

test('single descending sorter on ApplicationNo applied correctly', () => {
  const update = (data) => {
    var compareFunc = convertSortingAttributeNameToComparisonFunction("ApplicationNo")
    for(var i=0; i<Object.keys(data).length-1; i++)
    {
      var comparisonvalue = compareFunc(data[i], data[i+1])
      expect(comparisonvalue).toBeGreaterThanOrEqual(0)
    } 
  }
  render(<Menu cachedData={DummyData} updateTable={update} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  const selectedAttribute = screen.queryByTestId('sort-select-attr')
  fireEvent.change(selectedAttribute, { target: { value: "ApplicationNo" } })
  const selectedOrder = screen.getByTestId('sort-select-order')
  fireEvent.change(selectedOrder, { target: { value: "desc" } })

  // temp neccessarry to change filter state, otherwise no sorting is applied
  const select = screen.queryByTestId('filter-select')
  fireEvent.change(select, { target: { value: 'CMA' } })
  const textBox = screen.getByRole('textbox')
  fireEvent.change(textBox, { target: { value: 'no' } })
  fireEvent.focusOut(textBox)
  //

  fireEvent.click(screen.getByText(/Apply/i))
})

test('single ascending sorter on DecisionDate applied correctly', () => {
  const update = (data) => {
    var compareFunc = convertSortingAttributeNameToComparisonFunction("DecisionDate")
    for(var i=0; i<Object.keys(data).length-1; i++)
    {
      var comparisonvalue = compareFunc(data[i], data[i+1])
      expect(comparisonvalue).toBeLessThanOrEqual(0)
    } 
  }
  render(<Menu cachedData={DummyData} updateTable={update} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  const selectedAttribute = screen.queryByTestId('sort-select-attr')
  fireEvent.change(selectedAttribute, { target: { value: "DecisionDate" } })
  const selectedOrder = screen.getByTestId('sort-select-order')
  fireEvent.change(selectedOrder, { target: { value: "asc" } })

  // temp neccessarry to change filter state, otherwise no sorting is applied
  const select = screen.queryByTestId('filter-select')
  fireEvent.change(select, { target: { value: 'CMA' } })
  const textBox = screen.getByRole('textbox')
  fireEvent.change(textBox, { target: { value: 'no' } })
  fireEvent.focusOut(textBox)
  //

  fireEvent.click(screen.getByText(/Apply/i))
})
/* //test to check if sorting ascending on DecisionDate (special sorting case) works
test('single sorter on DecisionDate applied correctly', () => {
  const update = (data) => {
    var compareFunc = getSortingFunctionFromAttributeName("DecisionDate")
    for(var i=0; i<Object.keys(data).length-1; i++)
    {
      expect(compareFunc(data[i]["DecisionDate"], data[i+1]["DecisionDate"])).toBeLessThanOrEqual(0)
    } 
  }
  render(<Menu cachedData={DummyData} updateTable={update} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  const selectedAttribute = screen.queryByTestId('sort-select-attr')
  fireEvent.change(selectedAttribute, { target: { value: "DecisionDate" } })
  const selectedOrder = screen.getByTestId('sort-select-order')
  fireEvent.change(selectedOrder, { target: { value: "asc" } })
  fireEvent.click(screen.getByText(/Apply/i))
})

//test to check if sorting descending on MAH (special sorting case) works
test('single sorter on MAH applied correctly', () => {
  const update = (data) => {
    var compareFunc = getSortingFunctionFromAttributeName("MAH")
    for(var i=0; i<Object.keys(data).length-1; i++)
    {
      expect(compareFunc(data[i]["MAH"], data[i+1]["MAH"])).toBeMoreThanOrEqual(0)
    } 
  }
  render(<Menu cachedData={DummyData} updateTable={update} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  const selectedAttribute = screen.queryByTestId('sort-select-attr')
  fireEvent.change(selectedAttribute, { target: { value: "MAH" } })
  const selectedOrder = screen.getByTestId('sort-select-order')
  fireEvent.change(selectedOrder, { target: { value: "desc" } })
  fireEvent.click(screen.getByText(/Apply/i))
})

//test to check if sorting descending on ActiveSubstance (special sorting case) works
test('single sorter on ActiveSubstance applied correctly', () => {
  const update = (data) => {
    var compareFunc = getSortingFunctionFromAttributeName("ActiveSubstance")
    for(var i=0; i<Object.keys(data).length-1; i++)
    {
      expect(compareFunc(data[i]["ActiveSubstance"], data[i+1]["ActiveSubstance"])).toBeMoreThanOrEqual(0)
    } 
  }
  render(<Menu cachedData={DummyData} updateTable={update} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  const selectedAttribute = screen.queryByTestId('sort-select-attr')
  fireEvent.change(selectedAttribute, { target: { value: "ActiveSubstance" } })
  const selectedOrder = screen.getByTestId('sort-select-order')
  fireEvent.change(selectedOrder, { target: { value: "desc" } })
  fireEvent.click(screen.getByText(/Apply/i))
}) */
// data-testid="sort-select-order" data-testid="sort-select-attr"
/* // replace by individual attribute sorting tests=> unit tests
// make sorting checkkk data-testid="sort-select-order" data-testid="sort-select-attr"
test('single sorter applied correctly', () => {

  function geupdateDataCheck(data, attribuut, sortingorder) {
    var sortFuncForAttribute = getSortingFunctionFromAttributeName(attribuut)

    for(var i=0; i< data.Length-1; i++ )
    {
      expect(sortFuncForAttribute(DummyData[i], DummyData[i+1])).toBelessThanOrEqual(0)
    }
  }
  var sortingorders = ["asc", "desc"]
  var allattributes = Object.keys(DummyData[0])
  allattributes.forEach((attribuut) => {

    sortingorders.forEach((sortingorder) =>{
      
      render(<Menu cachedData={DummyData} updateTable={geupdateDataCheck(this.props.data, attribuut, sortingorder)} />)
      fireEvent.click(screen.getByText(/Filter & Sort/i))
      const selectedAttribute = screen.queryByTestId('sort-select-attr')
      fireEvent.change(selectedAttribute, { target: { value: attribuut } })
      const selectedOrder = screen.getByTestId('sort-select-order')
      fireEvent.change(selectedOrder, { target: { value: sortingorder } })
      fireEvent.click(screen.getByText(/Apply/i))
    })
  })
})
// */

test('two filters applied correctly', () => {
  const update = (data) => {
    data.forEach((element) => {
      expect(element.ApplicationNo.toString()).toContain('7')
      expect(element.DecisionYear.toString()).toContain('2001')
    })
  }
  render(<Menu cachedData={DummyData} updateTable={update} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  const firstSelect = screen.queryByTestId('filter-select')
  fireEvent.change(firstSelect, { target: { value: 'ApplicationNo' } })
  const firstText = screen.getByRole('textbox')
  fireEvent.change(firstText, { target: { value: '7' } })
  fireEvent.focusOut(firstText)
  fireEvent.click(screen.getByText(/Add Filter/i))
  const secondSelect = screen.queryAllByTestId('filter-select')[1]
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
  const firstSelect = screen.queryByTestId('filter-select')
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
  const select = screen.queryByTestId('filter-select')
  fireEvent.change(select, { target: { value: 'ApplicationNo' } })
  const text = screen.getByRole('textbox')
  fireEvent.change(text, { target: { value: '10' } })
  fireEvent.click(screen.getByText(/Close/i))
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  expect(select.value).toBe('ApplicationNo')
  expect(text.value).toBe('10')
})
