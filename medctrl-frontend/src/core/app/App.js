import './App.css'
import { BrowserRouter } from 'react-router-dom'
import SideNavigation from '../navigation/Navigation'
import AllRoutes from '../routes/AllRoutes.js'
import Header from '../header/Header'
import Footer from '../footer/Footer'

const userLoggedIn = true
const defUser = {
  isAdmin: true,
  userName: 'Lourens Bloem',
  accessLevel: 'X',
}

function App() {
  return (
    <BrowserRouter basename={process.env.PUBLIC_URL} >
      <div className="page__wrapper">
        <Header />
        <SideNavigation loggedin={userLoggedIn} user={defUser} />

        <main className="content">
          <div id="content__wrapper">
            <AllRoutes />
          </div>
          <Footer />
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App
