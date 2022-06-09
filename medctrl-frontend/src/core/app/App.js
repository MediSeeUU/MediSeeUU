import './App.css'
import { BrowserRouter } from 'react-router-dom'
import SideNavigation from '../navigation/Navigation'
import Routing from '../Routing.js'
import Header from '../header/Header'
import Footer from '../footer/Footer'
import Provider from '../../shared/Provider'
import DashboardTour from '../tour/DashboardTour'
import React from 'react'

function App() {
  return (
    <BrowserRouter basename={process.env.PUBLIC_URL}>
      <div className="med-page-wrapper">
        <Header />
        <SideNavigation />
        <main className="med-content">
          <div className="med-content-wrapper">
            <Provider>
              <DashboardTour>
                <Routing />
              </DashboardTour>
            </Provider>
          </div>
          <Footer />
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App
