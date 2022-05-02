import DummyData from '../../../../testJson/data.json'
import sortData, { convertSortingAttributeNameToComparisonFunction } from '../sorting'

//test to check if single parameter sorting ascending on ApplicationNo (number) works
test('single ascending sorter on ApplicationNo applied correctly', () => {
  let sortedData = sortData(DummyData, [{ selected: 'ApplicationNo', order: 'asc' }])
  var compareFunc = convertSortingAttributeNameToComparisonFunction('ApplicationNo')
  for (var i = 0; i < Object.keys(sortedData).length - 1; i++) {
    var comparisonvalue = compareFunc(sortedData[i], sortedData[i + 1])
    expect(comparisonvalue).toBeLessThanOrEqual(0)
  }
})

//test to check if single descending sorting on ApplicationNo works correctly
test('single descending sorter on ApplicationNo applied correctly', () => {
  let sortedData = sortData(DummyData, [{ selected: 'ApplicationNo', order: 'desc' }])
  var compareFunc = convertSortingAttributeNameToComparisonFunction('ApplicationNo')
  for (var i = 0; i < Object.keys(sortedData).length - 1; i++) {
    var comparisonvalue = compareFunc(sortedData[i], sortedData[i + 1])
    expect(comparisonvalue).toBeGreaterThanOrEqual(0)
  }
})

//Test to see if single ascending sorting on Decisiondate (special sort case) works correctly
test('single ascending sorter on DecisionDate applied correctly', () => {
  let sortedData = sortData(DummyData, [{ selected: 'DecisionDate', order: 'asc' }])
  var compareFunc = convertSortingAttributeNameToComparisonFunction('DecisionDate')
  for (var i = 0; i < Object.keys(sortedData).length - 1; i++) {
    var comparisonvalue = compareFunc(sortedData[i], sortedData[i + 1])
    expect(comparisonvalue).toBeLessThanOrEqual(0)
  }
})

//test to check if sorting ascending on MAH (special sorting case) works
test('single ascending sorter on MAH applied correctly', () => {
  let sortedData = sortData(DummyData, [{ selected: 'MAH', order: 'asc' }])
  var compareFunc = convertSortingAttributeNameToComparisonFunction('MAH')
  for (var i = 0; i < Object.keys(sortedData).length - 1; i++) {
    var comparisonvalue = compareFunc(sortedData[i], sortedData[i + 1])
    expect(comparisonvalue).toBeLessThanOrEqual(0)
  }
})

//test to check if sorting ascending on ActiveSubstance (special sorting case) works
test('single ascending sorter on ActiveSubstance (special case) applied correctly', () => {
  let sortedData = sortData(DummyData, [{ selected: 'ActiveSubstance', order: 'asc' }])
  var compareFunc = convertSortingAttributeNameToComparisonFunction('ActiveSubstance')
  for (var i = 0; i < Object.keys(sortedData).length - 1; i++) {
    var comparisonvalue = compareFunc(sortedData[i], sortedData[i + 1])
    expect(comparisonvalue).toBeLessThanOrEqual(0)
  }
})

//test to check if sorting first on ascending CMA and next on asc ActiveSubstance (special sorting case) works
test('double ascending sorters on 1:CMA 2:Activesubstance (special case) applied correctly', () => {
  let sortedData = sortData(DummyData, [{ selected: 'CMA', order: 'asc' }, { selected: 'ActiveSubstance', order: 'asc' }])
  var compareFunc1 = convertSortingAttributeNameToComparisonFunction('CMA')
  var compareFunc2 = convertSortingAttributeNameToComparisonFunction('ActiveSubstance')
  for (var i = 0; i < Object.keys(sortedData).length - 1; i++) {
    var comparisonvalue1 = compareFunc1(sortedData[i], sortedData[i + 1])
    expect(comparisonvalue1).toBeLessThanOrEqual(0)

    var comparisonvalue2 = 0
    if (comparisonvalue1 === 0) {
      comparisonvalue2 = compareFunc2(sortedData[i], sortedData[i + 1])
    }
    expect(comparisonvalue2).toBeLessThanOrEqual(0)
  }
})

//test to check if sorting first on ascending CMA and next on asc ApplicationNo (special sorting case) works
test('double ascending sorters on 1:CMA 2:ApplicationNo (special case) applied correctly', () => {
  let sortedData = sortData(DummyData, [{ selected: 'CMA', order: 'asc' }, { selected: 'ApplicationNo', order: 'asc' }])
  var compareFunc1 = convertSortingAttributeNameToComparisonFunction('CMA')
  var compareFunc2 = convertSortingAttributeNameToComparisonFunction('ApplicationNo')
  for (var i = 0; i < Object.keys(sortedData).length - 1; i++) {
    var comparisonvalue1 = compareFunc1(sortedData[i], sortedData[i + 1])
    expect(comparisonvalue1).toBeLessThanOrEqual(0)

    var comparisonvalue2 = 0
    if (comparisonvalue1 === 0) {
      comparisonvalue2 = compareFunc2(sortedData[i], sortedData[i + 1])
    }
    expect(comparisonvalue2).toBeLessThanOrEqual(0)
  }
})

//test to see error handeling when no attribute to sort on has been selected
//test to check if sorting ascending on ActiveSubstance (special sorting case) works
test('single ascending sorter on unselected Attribute error handled correctly', () => {
  let sortedData = sortData(DummyData, [{ selected: '', order: 'asc' }])
  var compareFunc = convertSortingAttributeNameToComparisonFunction('')
  for (var i = 0; i < Object.keys(sortedData).length - 1; i++) {
    var comparisonvalue = compareFunc(sortedData[i], sortedData[i + 1])
    expect(comparisonvalue).toBeLessThanOrEqual(0)
  }
})
