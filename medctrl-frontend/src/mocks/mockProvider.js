import Provider from "../shared/Provider"

function MockProvider({ children }) {
  return (
    <Provider mock={true}>
      {children}
    </Provider>
  )
}

export default MockProvider
