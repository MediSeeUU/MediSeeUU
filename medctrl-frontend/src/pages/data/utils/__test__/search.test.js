// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import searchData from '../search'
import DummyData from '../../../../json/data.json'

const columnSelection = ['EUNoShort', 'BrandName', 'MAH', 'DecisionDate']

test('query results in right search results', () => {
  let updatedData = searchData(DummyData, '10', columnSelection)
  updatedData.forEach((element) => {
    let inText = false
    Object.values(element).forEach((value) => {
      if (value.toString().toLowerCase().includes('10')) {
        inText = true
      }
    })
    expect(inText).toBe(true)
  })
})
