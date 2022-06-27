// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import filterData from '../filter'
import DummyData from '../../../../json/data.json'

test('single text filter applied correctly', () => {
  let filteredData = filterData(DummyData, [
    { selected: 'ApplicationNo', input: [{ var: '8' }], filterType: 'string' },
  ])
  filteredData.forEach((element) => {
    expect(element.ApplicationNo.toString()).toContain('8')
  })
})

test('single text filter applied correctly with category', () => {
  let filteredData = filterData(DummyData, [
    { selected: 'ApplicationNo', input: [{ var: '8', custom: true }], filterType: 'string' },
  ])
  filteredData.forEach((element) => {
    expect(element.ApplicationNo.toString()).toContain('8')
  })
})

test('two text filters applied correctly', () => {
  let filteredData = filterData(DummyData, [
    { selected: 'ApplicationNo', input: [{ var: '7' }], filterType: 'string' },
    {
      selected: 'DecisionYear',
      input: [{ var: '2001' }],
      filterType: 'string',
    },
  ])
  filteredData.forEach((element) => {
    expect(element.ApplicationNo.toString()).toContain('7')
    expect(element.DecisionYear.toString()).toContain('2001')
  })
})

test('multiple values in text filter applied correctly', () => {
  let filteredData = filterData(DummyData, [
    {
      selected: 'DecisionYear',
      input: [{ var: '1997' }, { var: '2001' }],
      filterType: 'string',
    },
  ])
  filteredData.forEach((element) => {
    expect(element.DecisionYear.toString()).toMatch(/(1997|2001)/i)
  })
})

test('single number filter applied correctly', () => {
  let filteredData = filterData(DummyData, [
    {
      selected: 'ApplicationNo',
      input: [{ var: '8', filterRange: 'from' }],
      filterType: 'number',
    },
  ])
  filteredData.forEach((element) => {
    expect(element.ApplicationNo).toBeGreaterThanOrEqual(8)
  })
})

test('two number filters applied correctly', () => {
  let filteredData = filterData(DummyData, [
    {
      selected: 'ApplicationNo',
      input: [{ var: '2000', filterRange: 'from' }],
      filterType: 'number',
    },
    {
      selected: 'DecisionYear',
      input: [{ var: '2001', filterRange: 'till' }],
      filterType: 'number',
    },
  ])
  filteredData.forEach((element) => {
    expect(element.ApplicationNo).toBeGreaterThanOrEqual(2000)
    expect(element.DecisionYear).toBeLessThanOrEqual(2001)
  })
})

test('multiple values in number filter applied correctly', () => {
  let filteredData = filterData(DummyData, [
    {
      selected: 'DecisionYear',
      input: [
        { var: '1997', filterRange: 'from' },
        { var: '2001', filterRange: 'till' },
      ],
      filterType: 'number',
    },
  ])
  filteredData.forEach((element) => {
    expect(parseInt(element.DecisionYear)).toBeGreaterThanOrEqual(1997)
    expect(parseInt(element.DecisionYear)).toBeLessThanOrEqual(2001)
  })
})

test('single date filter applied correctly', () => {
  let filteredData = filterData(DummyData, [
    {
      selected: 'DecisionDate',
      input: [{ var: '2012-03-20', filterRange: 'from' }],
      filterType: 'date',
    },
  ])
  filteredData.forEach((element) => {
    const elDate = new Date(element.DecisionDate)
    expect(elDate.getTime()).toBeGreaterThanOrEqual(
      new Date('2012-03-20').getTime()
    )
  })
})

test('two date filters applied correctly', () => {
  let filteredData = filterData(DummyData, [
    {
      selected: 'DecisionDate',
      input: [{ var: '2000-03-20', filterRange: 'from' }],
      filterType: 'date',
    },
    {
      selected: 'DecisionDate',
      input: [{ var: '2012-03-20', filterRange: 'till' }],
      filterType: 'date',
    },
  ])
  filteredData.forEach((element) => {
    const elDate = new Date(element.DecisionDate)
    expect(elDate.getTime()).toBeGreaterThanOrEqual(
      new Date('2000-03-20').getTime()
    )
    expect(elDate.getTime()).toBeLessThanOrEqual(
      new Date('2012-03-20').getTime()
    )
  })
})

test('multiple values in date filter applied correctly', () => {
  let filteredData = filterData(DummyData, [
    {
      selected: 'DecisionDate',
      input: [
        { var: '2000-03-20', filterRange: 'from' },
        { var: '2012-03-20', filterRange: 'till' },
      ],
      filterType: 'string',
    },
  ])
  filteredData.forEach((element) => {
    const elDate = new Date(element.DecisionDate)
    expect(elDate.getTime()).toBeGreaterThanOrEqual(
      new Date('2000-03-20').getTime()
    )
    expect(elDate.getTime()).toBeLessThanOrEqual(
      new Date('2012-03-20').getTime()
    )
  })
})

test('single bool filter applied correctly', () => {
  let filteredData = filterData(DummyData, [
    { selected: 'ATMP', input: [{ var: 'yes' }], filterType: 'bool' },
  ])
  filteredData.forEach((element) => {
    expect(element.ATMP.toString()).toStrictEqual('yes')
  })
})

test('two bool filters applied correctly', () => {
  let filteredData = filterData(DummyData, [
    { selected: 'ATMP', input: [{ var: 'yes' }], filterType: 'bool' },
    { selected: 'NASQualified', input: [{ var: 'no' }], filterType: 'bool' },
  ])
  filteredData.forEach((element) => {
    expect(element.ATMP.toString()).toStrictEqual('yes')
    expect(element.NASQualified.toString()).toStrictEqual('no')
  })
})

test('multiple values in bool filter applied correctly', () => {
  let filteredData = filterData(DummyData, [
    {
      selected: 'ATMP',
      input: [{ var: 'yes' }, { var: 'no' }],
      filterType: 'bool',
    },
  ])

  // filtering on a bool for both true and false, should give the original dataset back.
  expect(filteredData).toStrictEqual(DummyData)
  filteredData.forEach((element) => {
    expect(
      element.ATMP.toString() === 'yes' || element.ATMP.toString() === 'no'
    ).toBeTruthy()
    //expect(element.ATMP.toString()).toStrictEqual('yes').or.toStrictEqual('no')
  })
})
