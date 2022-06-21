// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import './App.css'
import { BrowserRouter } from 'react-router-dom'
import SideNavigation from '../navigation/Navigation'
import Routing from '../Routing.js'
import Header from '../header/Header'
import Footer from '../footer/Footer'
import Provider from '../../shared/Provider'
import DashboardTour from '../tour/DashboardTour'
import React from 'react'

// Function based component rendering the application and its components
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
