import DummyData from '../../../../json/data.json'
import sortData, {
  convertSortingAttributeNameToComparisonFunction,
} from '../sorting'

//test to check if single parameter sorting ascending on ApplicationNo (number) works
test('single ascending sorter on ApplicationNo applied correctly', () => {
  let sortedData = sortData(DummyData, [
    { selected: 'ApplicationNo', order: 'asc' },
  ])
  var compareFunc = convertSortingAttributeNameToComparisonFunction(
    'ApplicationNo',
    'asc'
  )
  for (var i = 0; i < Object.keys(sortedData).length - 1; i++) {
    var comparisonvalue = compareFunc(sortedData[i], sortedData[i + 1])
    expect(comparisonvalue).toBeLessThanOrEqual(0)
  }
})

//test to check if single parameter sorting ascending on LegalType works
test('single ascending sorter onLegalType applied correctly', () => {
  let sortedData = sortData(DummyData, [
    { selected: 'LegalType', order: 'asc' },
  ])
  const NAvalues = ['NA', 'unknown', 'na', 'null']
  var compareFunc = convertSortingAttributeNameToComparisonFunction(
    'LegalType',
    'asc'
  )
  for (var i = 0; i < Object.keys(sortedData).length - 1; i++) {
    var comparisonvalue = 0
    //escape hatch; if value of attribute is in NAvalues, sortingfunction will always return 1 (if asc order),
    // or -1 (if desc order), to ensure NA values are always placed last.
    if (
      NAvalues.includes(sortedData[i]['LegalType']) ||
      NAvalues.includes(sortedData[i + 1]['LegalType'])
    ) {
      comparisonvalue = 0
    } else {
      comparisonvalue = compareFunc(sortedData[i], sortedData[i + 1])
    }
    expect(comparisonvalue).toBeLessThanOrEqual(0)
  }
})

//test to check if single descending sorting on ApplicationNo works correctly
test('single descending sorter on ApplicationNo applied correctly', () => {
  let sortedData = sortData(DummyData, [
    { selected: 'ApplicationNo', order: 'desc' },
  ])
  var compareFunc = convertSortingAttributeNameToComparisonFunction(
    'ApplicationNo',
    'desc'
  )
  for (var i = 0; i < Object.keys(sortedData).length - 1; i++) {
    var comparisonvalue = compareFunc(sortedData[i], sortedData[i + 1])
    expect(comparisonvalue).toBeGreaterThanOrEqual(0)
  }
})

//Test to see if single ascending sorting on Decisiondate (special sort case) works correctly
test('single ascending sorter on DecisionDate applied correctly', () => {
  let sortedData = sortData(DummyData, [
    { selected: 'DecisionDate', order: 'asc' },
  ])
  var compareFunc = convertSortingAttributeNameToComparisonFunction(
    'DecisionDate',
    'asc'
  )
  for (var i = 0; i < Object.keys(sortedData).length - 1; i++) {
    var comparisonvalue = compareFunc(sortedData[i], sortedData[i + 1])
    expect(comparisonvalue).toBeLessThanOrEqual(0)
  }
})

//test to check if sorting ascending on MAH (special sorting case) works
test('single ascending sorter on MAH applied correctly', () => {
  let sortedData = sortData(DummyData, [{ selected: 'MAH', order: 'asc' }])
  var compareFunc = convertSortingAttributeNameToComparisonFunction(
    'MAH',
    'asc'
  )
  for (var i = 0; i < Object.keys(sortedData).length - 1; i++) {
    var comparisonvalue = compareFunc(sortedData[i], sortedData[i + 1])
    expect(comparisonvalue).toBeLessThanOrEqual(0)
  }
})

//test to check if sorting ascending on ActiveSubstance (special sorting case) works
test('single ascending sorter on ActiveSubstance (special case) applied correctly', () => {
  let sortedData = sortData(DummyData, [
    { selected: 'ActiveSubstance', order: 'asc' },
  ])
  var compareFunc = convertSortingAttributeNameToComparisonFunction(
    'ActiveSubstance',
    'asc'
  )
  for (var i = 0; i < Object.keys(sortedData).length - 1; i++) {
    var comparisonvalue = compareFunc(sortedData[i], sortedData[i + 1])
    expect(comparisonvalue).toBeLessThanOrEqual(0)
  }
})

//test to check if first sorting on ATMP and for any equal tuples then sort on activesubstance
test('double ascending sorters on 1:ATMP 2:Activesubstance applied correctly', () => {
  let sortedData = sortData(DummyData, [
    { selected: 'ATMP', order: 'asc' },
    { selected: 'ActiveSubstance', order: 'asc' },
  ])
  var compareFunc1 = convertSortingAttributeNameToComparisonFunction(
    'ATMP',
    'asc'
  )
  var compareFunc2 = convertSortingAttributeNameToComparisonFunction(
    'ActiveSubstance',
    'asc'
  )
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

//test to check if first sorting on atmp and next sort any equal attributes on applicationNo
test('double ascending sorters on 1:ATMP 2:ApplicationNo applied correctly', () => {
  let sortedData = sortData(DummyData, [
    { selected: 'ATMP', order: 'asc' },
    { selected: 'ApplicationNo', order: 'asc' },
  ])
  var compareFunc1 = convertSortingAttributeNameToComparisonFunction(
    'ATMP',
    'asc'
  )
  var compareFunc2 = convertSortingAttributeNameToComparisonFunction(
    'ApplicationNo',
    'asc'
  )
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

//test to check if sorting function is able to errorhandle no attribute selected
test('single ascending sorter on unselected Attribute error handled correctly', () => {
  let sortedData = sortData(DummyData, [{ selected: '', order: 'asc' }])
  var compareFunc = convertSortingAttributeNameToComparisonFunction('', 'asc')
  for (var i = 0; i < Object.keys(sortedData).length - 1; i++) {
    var comparisonvalue = compareFunc(sortedData[i], sortedData[i + 1])
    expect(comparisonvalue).toBeLessThanOrEqual(0)
  }
})
