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
import DummyData from '../../../testJson/data.json'
import {
  convertSortingAttributeNameToComparisonFunction,
  getSortingFunctionFromAttributeName,
} from '../sorting'

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

// test for checking if clicking the X button to remove sorting option removes an sorting-item when this item is not the last sorting box (A)
test('remove sorting option removes sorting item', () => {
  render(<Menu cachedData={DummyData} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  //add 2nd sorting option box
  fireEvent.click(screen.getByText(/Add Sorting option +/i))
  expect(screen.queryAllByTestId('sort-select-attr')).toHaveLength(2)
  //remove the second option sorting box only
  fireEvent.click(screen.getAllByTestId('delete-sorting-box')[1])
  expect(screen.queryAllByTestId('sort-select-attr')).toHaveLength(1)
})

//test to check if single parameter sorting ascending on ApplicationNo (number) works
test('single ascending sorter on ApplicationNo applied correctly', () => {
  const update = (data) => {
    var compareFunc =
      convertSortingAttributeNameToComparisonFunction('ApplicationNo')
    for (var i = 0; i < Object.keys(data).length - 1; i++) {
      var comparisonvalue = compareFunc(data[i], data[i + 1])
      expect(comparisonvalue).toBeLessThanOrEqual(0)
    }
  }
  render(<Menu cachedData={DummyData} updateTable={update} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  const selectedAttribute = screen.queryByTestId('sort-select-attr')
  fireEvent.change(selectedAttribute, { target: { value: 'ApplicationNo' } })
  const selectedOrder = screen.getByTestId('sort-select-order')
  fireEvent.change(selectedOrder, { target: { value: 'asc' } })

  // temp neccessarry to change filter state, otherwise no sorting is applied
  const select = screen.queryByTestId('filter-select')
  fireEvent.change(select, { target: { value: 'CMA' } })
  const textBox = screen.getByRole('textbox')
  fireEvent.change(textBox, { target: { value: 'no' } })
  fireEvent.focusOut(textBox)
  //

  fireEvent.click(screen.getByText(/Apply/i))
})

//test to check if single parameter sorting ascending on ApplicationNo (number) works ARRAYS
test('single ascending sorter on ApplicationNo applied correctly, FOR ARRAYS', () => {
  const update = (data) => {
    var compareFunc = getSortingFunctionFromAttributeName('ApplicationNo')
    for (var i = 0; i < Object.keys(data).length - 1; i++) {
      var comparisonvalue = compareFunc(
        data[i]['ApplicationNo'],
        data[i + 1]['ApplicationNo']
      )
      expect(comparisonvalue).toBeLessThanOrEqual(0)
    }
  }
  render(<Menu cachedData={DummyData} updateTable={update} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  const selectedAttribute = screen.queryByTestId('sort-select-attr')
  fireEvent.change(selectedAttribute, { target: { value: 'ApplicationNo' } })
  const selectedOrder = screen.getByTestId('sort-select-order')
  fireEvent.change(selectedOrder, { target: { value: 'asc' } })

  // temp neccessarry to change filter state, otherwise no sorting is applied
  const select = screen.queryByTestId('filter-select')
  fireEvent.change(select, { target: { value: 'CMA' } })
  const textBox = screen.getByRole('textbox')
  fireEvent.change(textBox, { target: { value: 'no' } })
  fireEvent.focusOut(textBox)
  //

  fireEvent.click(screen.getByText(/Apply/i))
})

//test to check if single descending sorting on ApplicationNo works correctly
test('single descending sorter on ApplicationNo applied correctly', () => {
  const update = (data) => {
    var compareFunc =
      convertSortingAttributeNameToComparisonFunction('ApplicationNo')
    for (var i = 0; i < Object.keys(data).length - 1; i++) {
      var comparisonvalue = compareFunc(data[i], data[i + 1])
      expect(comparisonvalue).toBeGreaterThanOrEqual(0)
    }
  }
  render(<Menu cachedData={DummyData} updateTable={update} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  const selectedAttribute = screen.queryByTestId('sort-select-attr')
  fireEvent.change(selectedAttribute, { target: { value: 'ApplicationNo' } })
  const selectedOrder = screen.getByTestId('sort-select-order')
  fireEvent.change(selectedOrder, { target: { value: 'desc' } })

  // temp neccessarry to change filter state, otherwise no sorting is applied
  const select = screen.queryByTestId('filter-select')
  fireEvent.change(select, { target: { value: 'CMA' } })
  const textBox = screen.getByRole('textbox')
  fireEvent.change(textBox, { target: { value: 'no' } })
  fireEvent.focusOut(textBox)
  //

  fireEvent.click(screen.getByText(/Apply/i))
})
//Test to see if single ascending sorting on Decisiondate (special sort case) works correctly
test('single ascending sorter on DecisionDate applied correctly', () => {
  const update = (data) => {
    var compareFunc =
      convertSortingAttributeNameToComparisonFunction('DecisionDate')
    for (var i = 0; i < Object.keys(data).length - 1; i++) {
      var comparisonvalue = compareFunc(data[i], data[i + 1])
      expect(comparisonvalue).toBeLessThanOrEqual(0)
    }
  }
  render(<Menu cachedData={DummyData} updateTable={update} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  const selectedAttribute = screen.queryByTestId('sort-select-attr')
  fireEvent.change(selectedAttribute, { target: { value: 'DecisionDate' } })
  const selectedOrder = screen.getByTestId('sort-select-order')
  fireEvent.change(selectedOrder, { target: { value: 'asc' } })

  // temp neccessarry to change filter state, otherwise no sorting is applied
  const select = screen.queryByTestId('filter-select')
  fireEvent.change(select, { target: { value: 'CMA' } })
  const textBox = screen.getByRole('textbox')
  fireEvent.change(textBox, { target: { value: 'no' } })
  fireEvent.focusOut(textBox)
  //

  fireEvent.click(screen.getByText(/Apply/i))
})
//test to check if sorting ascending on MAH (special sorting case) works
test('single ascending sorter on MAH applied correctly', () => {
  const update = (data) => {
    var compareFunc = convertSortingAttributeNameToComparisonFunction('MAH')
    for (var i = 0; i < Object.keys(data).length - 1; i++) {
      var comparisonvalue = compareFunc(data[i], data[i + 1])
      expect(comparisonvalue).toBeLessThanOrEqual(0)
    }
  }
  render(<Menu cachedData={DummyData} updateTable={update} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  const selectedAttribute = screen.queryByTestId('sort-select-attr')
  fireEvent.change(selectedAttribute, { target: { value: 'MAH' } })
  const selectedOrder = screen.getByTestId('sort-select-order')
  fireEvent.change(selectedOrder, { target: { value: 'asc' } })

  // temp neccessarry to change filter state, otherwise no sorting is applied
  const select = screen.queryByTestId('filter-select')
  fireEvent.change(select, { target: { value: 'CMA' } })
  const textBox = screen.getByRole('textbox')
  fireEvent.change(textBox, { target: { value: 'no' } })
  fireEvent.focusOut(textBox)
  //

  fireEvent.click(screen.getByText(/Apply/i))
})

//test to check if sorting ascending on ActiveSubstance (special sorting case) works
test('single ascending sorter on ActiveSubstance (special case) applied correctly', () => {
  const update = (data) => {
    var compareFunc =
      convertSortingAttributeNameToComparisonFunction('ActiveSubstance')
    for (var i = 0; i < Object.keys(data).length - 1; i++) {
      var comparisonvalue = compareFunc(data[i], data[i + 1])
      expect(comparisonvalue).toBeLessThanOrEqual(0)
    }
  }
  render(<Menu cachedData={DummyData} updateTable={update} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  const selectedAttribute = screen.queryByTestId('sort-select-attr')
  fireEvent.change(selectedAttribute, { target: { value: 'ActiveSubstance' } })
  const selectedOrder = screen.getByTestId('sort-select-order')
  fireEvent.change(selectedOrder, { target: { value: 'asc' } })

  // temp neccessarry to change filter state, otherwise no sorting is applied
  const select = screen.queryByTestId('filter-select')
  fireEvent.change(select, { target: { value: 'CMA' } })
  const textBox = screen.getByRole('textbox')
  fireEvent.change(textBox, { target: { value: 'no' } })
  fireEvent.focusOut(textBox)
  //

  fireEvent.click(screen.getByText(/Apply/i))
})

//test to check if sorting first on ascending CMA and next on asc ActiveSubstance (special sorting case) works
test('double ascending sorters on 1:CMA 2:Activesubstance (special case) applied correctly', () => {
  const update = (data) => {
    var compareFunc1 = convertSortingAttributeNameToComparisonFunction('CMA')
    var compareFunc2 =
      convertSortingAttributeNameToComparisonFunction('ActiveSubstance')
    for (var i = 0; i < Object.keys(data).length - 1; i++) {
      var comparisonvalue1 = compareFunc1(data[i], data[i + 1])
      expect(comparisonvalue1).toBeLessThanOrEqual(0)

      var comparisonvalue2 = 0
      if (comparisonvalue1 === 0) {
        comparisonvalue2 = compareFunc2(data[i], data[i + 1])
      }
      expect(comparisonvalue2).toBeLessThanOrEqual(0)
    }
  }

  //set first sorting option
  render(<Menu cachedData={DummyData} updateTable={update} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  const selectedAttribute = screen.queryAllByTestId('sort-select-attr')[0]
  fireEvent.change(selectedAttribute, { target: { value: 'CMA' } })
  const selectedOrder = screen.getAllByTestId('sort-select-order')[0]
  fireEvent.change(selectedOrder, { target: { value: 'asc' } })

  //set second sorting option
  fireEvent.click(screen.getByText(/Add Sorting option +/i))
  const selectedAttribute2 = screen.queryAllByTestId('sort-select-attr')[1]
  fireEvent.change(selectedAttribute2, { target: { value: 'ActiveSubstance' } })
  const selectedOrder2 = screen.getAllByTestId('sort-select-order')[1]
  fireEvent.change(selectedOrder2, { target: { value: 'asc' } })

  // temp neccessarry to change filter state, otherwise no sorting is applied
  const select = screen.queryByTestId('filter-select')
  fireEvent.change(select, { target: { value: 'AEC' } })
  const textBox = screen.getByRole('textbox')
  fireEvent.change(textBox, { target: { value: 'no' } })
  fireEvent.focusOut(textBox)
  //

  fireEvent.click(screen.getByText(/Apply/i))
})

//test to check if sorting first on ascending CMA and next on asc ApplicationNo (special sorting case) works
test('double ascending sorters on 1:CMA 2:ApplicationNo (special case) applied correctly', () => {
  const update = (data) => {
    var compareFunc1 = convertSortingAttributeNameToComparisonFunction('CMA')
    var compareFunc2 =
      convertSortingAttributeNameToComparisonFunction('ApplicationNo')
    for (var i = 0; i < Object.keys(data).length - 1; i++) {
      var comparisonvalue1 = compareFunc1(data[i], data[i + 1])
      expect(comparisonvalue1).toBeLessThanOrEqual(0)

      var comparisonvalue2 = 0
      if (comparisonvalue1 === 0) {
        comparisonvalue2 = compareFunc2(data[i], data[i + 1])
      }
      expect(comparisonvalue2).toBeLessThanOrEqual(0)
    }
  }

  //set first sorting option
  render(<Menu cachedData={DummyData} updateTable={update} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  const selectedAttribute = screen.queryAllByTestId('sort-select-attr')[0]
  fireEvent.change(selectedAttribute, { target: { value: 'CMA' } })
  const selectedOrder = screen.getAllByTestId('sort-select-order')[0]
  fireEvent.change(selectedOrder, { target: { value: 'asc' } })

  //set second sorting option
  fireEvent.click(screen.getByText(/Add Sorting option +/i))
  const selectedAttribute2 = screen.queryAllByTestId('sort-select-attr')[1]
  fireEvent.change(selectedAttribute2, { target: { value: 'ApplicationNo' } })
  const selectedOrder2 = screen.getAllByTestId('sort-select-order')[1]
  fireEvent.change(selectedOrder2, { target: { value: 'asc' } })

  // temp neccessarry to change filter state, otherwise no sorting is applied
  const select = screen.queryByTestId('filter-select')
  fireEvent.change(select, { target: { value: 'AEC' } })
  const textBox = screen.getByRole('textbox')
  fireEvent.change(textBox, { target: { value: 'no' } })
  fireEvent.focusOut(textBox)
  //

  fireEvent.click(screen.getByText(/Apply/i))
})

//test to see error handeling when no attribute to sort on has been selected
//test to check if sorting ascending on ActiveSubstance (special sorting case) works
test('single ascending sorter on unselected Attribute error handled correctly', () => {
  const update = (data) => {
    var compareFunc = convertSortingAttributeNameToComparisonFunction('')
    for (var i = 0; i < Object.keys(data).length - 1; i++) {
      var comparisonvalue = compareFunc(data[i], data[i + 1])
      expect(comparisonvalue).toBeLessThanOrEqual(0)
    }
  }
  render(<Menu cachedData={DummyData} updateTable={update} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  const selectedAttribute = screen.queryByTestId('sort-select-attr')
  fireEvent.change(selectedAttribute, { target: { value: '' } })
  const selectedOrder = screen.getByTestId('sort-select-order')
  fireEvent.change(selectedOrder, { target: { value: 'asc' } })

  // temp neccessarry to change filter state, otherwise no sorting is applied
  const select = screen.queryByTestId('filter-select')
  fireEvent.change(select, { target: { value: 'CMA' } })
  const textBox = screen.getByRole('textbox')
  fireEvent.change(textBox, { target: { value: 'no' } })
  fireEvent.focusOut(textBox)

  fireEvent.click(screen.getByText(/Apply/i))
})
//-------
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

test('max 4 filters', () => {
  render(<Menu cachedData={DummyData} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  const addSort = screen.getByText(/Add Sorting option +/i)
  fireEvent.click(addSort)
  fireEvent.click(addSort)
  fireEvent.click(addSort)
  expect(addSort).not.toBeInTheDocument()
})

test('add filterbox', () => {
  render(<Menu cachedData={DummyData} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  expect(screen.getAllByRole('textbox')).toHaveLength(1)
  fireEvent.click(screen.getByText('+ Add'))
  expect(screen.getAllByRole('textbox')).toHaveLength(2)
})

test('remove filterbox', () => {
  render(<Menu cachedData={DummyData} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  fireEvent.click(screen.getByText('+ Add'))
  expect(screen.getAllByRole('textbox')).toHaveLength(2)
  fireEvent.click(screen.getAllByTestId('remove-icon')[0])
  expect(screen.getAllByRole('textbox')).toHaveLength(1)
})

test('always have one filterbox', () => {
  render(<Menu cachedData={DummyData} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  expect(screen.getAllByRole('textbox')).toHaveLength(1)
  fireEvent.click(screen.getByTestId('remove-icon'))
  expect(screen.getAllByRole('textbox')).toHaveLength(1)
})

test('remove filter', () => {
  render(<Menu cachedData={DummyData} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  fireEvent.click(screen.getByText(/Add Filter/i))
  expect(screen.queryAllByTestId('filter-select')).toHaveLength(2)
  fireEvent.click(screen.getAllByTestId('delete-icon')[0])
  expect(screen.queryAllByTestId('filter-select')).toHaveLength(1)
})

test('always have one filter', () => {
  render(<Menu cachedData={DummyData} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  expect(screen.queryAllByTestId('filter-select')).toHaveLength(1)
  fireEvent.click(screen.getByTestId('delete-icon'))
  expect(screen.queryAllByTestId('filter-select')).toHaveLength(1)
})
