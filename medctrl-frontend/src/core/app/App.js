import './App.css'
import { BrowserRouter } from 'react-router-dom'
import SideNavigation from '../navigation/Navigation'
import AllRoutes from '../routes/AllRoutes.js'
import Header from '../header/Header'
import Footer from '../footer/Footer'

const userLoggedIn = true
const defUser = {
  isAdmin: false,
  userName: 'Lourens Bloem',
  accessLevel: 'X',
}

function App() {
  return (
    <BrowserRouter basename={process.env.PUBLIC_URL}>
      <div className="med_page__wrapper">
        <Header className="med_mainLayout" />
        <SideNavigation
          className="med_mainLayout"
          loggedin={userLoggedIn}
          user={defUser}
        />

        <main className="med_content">
          <div className="med_content__wrapper">
            <AllRoutes />
          </div>
          <Footer />
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App
