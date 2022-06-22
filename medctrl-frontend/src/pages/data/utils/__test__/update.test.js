// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import updateData from '../update'
import DummyData from '../../../../json/data.json'

const columnSelection = ['EUNoShort', 'BrandName', 'MAH', 'DecisionDate']

test('applying search, filters and sorters', () => {
  const updatedData = updateData(
    DummyData,
    {
      search: 'cell',
      filters: [
        {
          selected: 'EUNoShort',
          input: [{ var: '10' }, { var: '8' }],
          filterType: 'string',
        },
      ],
      sorters: [{ selected: 'Rapporteur', order: 'desc' }],
    },
    columnSelection
  )
  updatedData.forEach((element) => {
    // Test search
    const vals = Object.values(element)
    let inText = false
    for (const val of vals) {
      if (val.toString().toLowerCase().includes('cell')) {
        inText = true
      }
    }
    expect(inText).toBe(true)
    // Test filter
    expect(element.EUNoShort.toString()).toMatch(/(10|8)/i)
  })
  // Test sort
  const sortedData = updatedData.sort((a, b) =>
    b.Rapporteur.localeCompare(a.Rapporteur)
  )
  expect(updatedData).toEqual(sortedData)
})
