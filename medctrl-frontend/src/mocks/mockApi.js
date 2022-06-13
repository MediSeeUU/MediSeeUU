import { rest } from 'msw'
import { setupServer } from 'msw/node'
import sampleProcedureData from '../json/detailed-info-data.json'

// Create a mock API
// This is used to be able to unit test components that need certain data
const mockApi = setupServer(
  // Example of a request handler
  rest.get('/api/exampleMockRequest', (req, res, ctx) => {
    // Respond using mocked JSON
    return res(
      ctx.json({
        example: 'data',
      })
    )
  }),
  rest.get('/api/saveselection', (req, res, ctx) => {
    // Respond using a mocked JSON body
    return res(
      ctx.json([
        {
          id: '377932a8-63e6-4e77-bb0f-efc220eb6d25',
          name: 'test1',
          created_at: '2022-05-17T11:16:47.141360Z',
          created_by: 'admin',
          eunumbers: [1, 2, 3],
        },
        {
          id: '772268f6-1468-47a4-aff6-786d1a826c5b',
          name: 'test2',
          created_at: '2022-05-17T11:10:36.026106Z',
          created_by: 'admin',
          eunumbers: [4, 5, 6],
        },
        {
          id: '998d1243-802f-4af6-86aa-215d3679163e',
          name: 'test3',
          created_at: '2022-05-17T07:30:39.319753Z',
          created_by: 'admin',
          eunumbers: [7, 8, 9],
        },
      ])
    )
  }),
  rest.post('/api/account/login', (req, res, ctx) => {
    return res(
      ctx.json({
        expiry: '2022-05-18T22:27:47.764171Z',
        token:
          '824g1f222222229f356872b140e12564ebae39915728469286a8d3cac4eeadfc31',
        user: {
          id: 2,
          username: 'admin',
          groups: [
            {
              name: 'testG',
              id: 2,
            },
          ],
          selections: [],
        },
      })
    )
  }),
  rest.get('/api/procedure/:medID', (req, res, ctx) => {
    // Respond using a mocked JSON body
    return res(ctx.json(sampleProcedureData.procedures))
  })
)

beforeAll(() => mockApi.listen())
afterEach(() => mockApi.resetHandlers())
afterAll(() => mockApi.close())

export default mockApi
