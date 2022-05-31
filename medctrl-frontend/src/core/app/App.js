import './App.css'
import { BrowserRouter } from 'react-router-dom'
import SideNavigation from '../navigation/Navigation'
import Routing from '../Routing.js'
import Header from '../header/Header'
import Footer from '../footer/Footer'
import { DataProvider } from '../../shared/contexts/DataContext'
import DashboardTour from '../tour/DashboardTour'
import React from 'react'

function App() {
  return (
    <BrowserRouter basename={process.env.PUBLIC_URL}>
      <div className="med-page-wrapper">
        <DashboardTour>
          <Header />
          <SideNavigation />
          <main className="med-content">
            <div className="med-content-wrapper">
              <DataProvider>
                <Routing />
              </DataProvider>
            </div>
            <Footer />
          </main>
        </DashboardTour>
      </div>
    </BrowserRouter>
  )
}

export default App
