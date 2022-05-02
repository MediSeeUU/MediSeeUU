import updateData from '../update'
import DummyData from '../../../../testJson/data.json'

let columnSelection = [
  'EUNoShort',
  'BrandName',
  'MAH',
  'DecisionDate',
  'ATCNameL2',
]

test('applying search, filters and sorters', () => {
  const updatedData = updateData(DummyData, 'cell', [{ selected: 'EUNoShort', input: ['10', '8'] }], [{ selected: 'Rapporteur', order: 'desc' }], columnSelection)
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
  const sortedData = updatedData.sort((a, b) => b.Rapporteur.localeCompare(a.Rapporteur))
  expect(updatedData).toEqual(sortedData)
})
