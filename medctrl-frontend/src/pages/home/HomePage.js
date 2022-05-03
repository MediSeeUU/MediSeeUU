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
        <h1>Tools</h1>
        <hr className="med-top-separator" />
        <p>Explanation what can be done on every page</p>
      </div>

      <div className="med-content-container med_content__container">
        <h1>Instructions</h1>
        <hr className="med-top-separator" />

        <div>
          <h2>Data</h2>
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
