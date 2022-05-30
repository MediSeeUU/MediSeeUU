import './HomePage.css'
import '../../shared/shared.css'
import Search from '../../shared/Search/Search'
import { useNavigate } from 'react-router-dom'
import { useTourRun } from '../../core/tour/DashboardTour'
import {
 useTableUtils,
 useTableUtilsUpdate,
} from '../../shared/contexts/DataContext'

function HomePage() {
  const navigate = useNavigate()
  const runTour = useTourRun()

  let utils = useTableUtils()
  let utilsUpdate = useTableUtilsUpdate()

  // Set the query in the utils context and navigate to the datapage
  const search = (query) => {
   utilsUpdate({ ...utils, search: query })
   navigate('/data?q=' + query)
  }

  return (
    // Homepage components, contains search bar and article containers
    <div className="med-home-content">
      <div className="med-content-container">
        <h1>Dashboard Tour</h1>
        <hr className="med-top-separator" />

        <button
          className="med-primary-solid med-bx-button med-tour-button"
          onClick={() => runTour(true)}
        >
          <i className="bx bx-code-alt med-button-image" />
          Start Tour
        </button>

        <p className="med-tour-paragraph">
          To explore all the features of this dashboard, take a guided tour
          around the website by clicking the button. This tour will not take
          long and familiarize you with all the core functionalities that this
          dashboard has to offer. You can end the tour at any time by clicking
          'end'. When you reach the end of the tour, the tour will automatically
          finish.
        </p>
      </div>

      <Search tour="step-search" update={search} />

      <div className="med-content-container">
        <h1>Tools</h1>
        <hr className="med-top-separator" />
        <p>
          This dashboard provides tools for looking up, filtering, and
          visualizing data points regarding pharmaceutical policy and
          regulation. All functionality is split up into two pages: <i>Data</i>{' '}
          and <i>Visualize</i>.
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
            in on a subset of the diagram. For any diagram, all quantities are
            clickable, which allows for the export or removal of specific data
            points. The resulting visualization can be exported to a local image
            file if desired.
          </p>
        </div>
      </div>
    </div>
  )
}

export default HomePage
