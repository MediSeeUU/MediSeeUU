import filterData from '../filter'
import DummyData from '../../../../testJson/data.json'

test('single filter applied correctly', () => {
  let filteredData = filterData(DummyData, [
    { selected: 'ApplicationNo', input: [{var: '8'}], filterType: 'text' },
  ])
  filteredData.forEach((element) => {
    expect(element.ApplicationNo.toString()).toContain('8')
  })
})

test('two filters applied correctly', () => {
  let filteredData = filterData(DummyData, [
    { selected: 'ApplicationNo', input: [{var: '7'}], filterType: 'text' },
    { selected: 'DecisionYear', input: [{var: '2001'}], filterType: 'text' },
  ])
  filteredData.forEach((element) => {
    expect(element.ApplicationNo.toString()).toContain('7')
    expect(element.DecisionYear.toString()).toContain('2001')
  })
})

test('multiple values in filter applied correctly', () => {
  let filteredData = filterData(DummyData, [
    { selected: 'DecisionYear', input: [{var: '1997'}, {var: '2001'}], filterType: 'text' },
  ])
  filteredData.forEach((element) => {
    expect(element.DecisionYear.toString()).toMatch(/(1997|2001)/i)
  })
})
