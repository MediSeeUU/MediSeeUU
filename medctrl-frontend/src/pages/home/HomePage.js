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
        <p>
          This dashboard provides tools for looking up, filtering, and
          visualizing data points regarding pharmaceutical policy and
          regularization. All functionality is split up into two pages:{' '}
          <i>Data</i> and <i>Visualize</i>.
        </p>
        <div>
          <h2>Data</h2>
          <p>
            The data page is optimized to find data points quickly. Searching
            can be done based on keywords and letter combinations, but filters
            can also be applied to ensure that only data points that meet
            specific (parameter) requirements appear. The data points can be
            sorted by a parameter of your choice. Finally, a selection can be
            made manually from the remaining data points, which can be used for
            visualization or exported to a local file if desired.
          </p>
        </div>
        <div>
          <h2>Visualize</h2>
          <p>
            The data points selected on the data page can be displayed
            graphically on the visualization page. An unlimited amount of
            visualizations can be added, each with its own title. There are four
            types of charts to choose from: a bar chart, a line chart, a pie
            chart, and a histogram. For each of these chart types, it can be
            determined which variables are shown on the axes and whether labels
            or a legend should be shown. For these variables, you can choose
            which values/categories are shown or skipped in the diagram. For bar
            charts, you can also choose to display the chart horizontally and to
            stack the bars (“Stacked”) so that fewer bars need to be shown. If
            the latter is chosen, you can also choose to make all bars the same
            length (“Fully stacked”) so that the graph is expressed in relative
            quantities. For line charts and histograms, it is possible to zoom
            in on a subset of the diagram. The resulting visualization can be
            exported to a local image file if desired.
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
        <p className="visualization-description">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
          eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
          minim veniam, quis nostrud exercitation ullamco laboris nisi ut
          aliquip ex ea commodo consequat. Duis aute irure dolor in
          reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
          pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
          culpa qui officia deserunt mollit anim id est laborum.
        </p>
      </div>
    </div>
  )
}

export default HomePage
