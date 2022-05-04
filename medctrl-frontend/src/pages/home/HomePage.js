import './HomePage.css'
import '../../shared/shared.css'
import Search from '../../shared/Search/Search'
import { useNavigate } from 'react-router-dom'

function HomePage() {
  const navigate = useNavigate()
  return (
    // Homepage components, contains search bar and article containers
    <div className="med_home_content">
      <Search update={(query) => navigate('/data?q=' + query)} />

      <div className="med-content-container med_content__container">
        <h1>Dashboard</h1>
        <hr className="med-top-separator" />
        <p>
          In this dashboard, tools for looking up, filtering and visualizing
          data on medicines regulation are available. All functionality is split
          up into two pages: <i>Data</i> and <i>Visualize</i>.
        </p>
        <div>
          <h2>Data</h2>
          <p>Explanation what can be done on every page</p>
          <p className="institution-info">
            A step-by-step plan how to use the site (first search and filter
            data, make visualisations and export)
          </p>
        </div>
        <div>
          <h2>Visualize</h2>
          <p>Explanation what can be done on every page</p>
          <p className="institution-info">
            A step-by-step plan how to use the site (first search and filter
            data, make visualisations and export)
          </p>
        </div>
      </div>

      <div className="med-content-container med_content__container">
        <h1>Example of a visualization</h1>
        <hr className="med-top-separator" />
        <p>
          This must be a clear example such as a timeline of "orphan
          designations" per decisionyear (image).
        </p>
      </div>
    </div>
  )
}

export default HomePage
