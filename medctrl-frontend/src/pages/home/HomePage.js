import './HomePage.css'
import '../../shared/shared.css'
import Search from '../../shared/Search/Search'
import { useNavigate } from 'react-router-dom'

import uuLogo from '../../images/uu-logo.svg'
import mebLogo from '../../images/meb-logo.svg'
import { useTourRun } from '../../core/tour/DashboardTour'

function HomePage() {
  const navigate = useNavigate()
  const runTour = useTourRun()
  return (
    // Homepage components, contains article containers (styling in HomePage.css)
    <div className="med_home_content">
      <div className="med-content-container">
        <h1>Dashboard Tour</h1>
        <hr className="med-top-separator" />

        <button
          className="med-primary-solid med-bx-button med-tour-button"
          onClick={() => runTour(true)}
        >
          <i className="bx bx-code-alt search-Icon" />
          Start Tour
        </button>

        <p className="med-tour-paragraph">
          To explore all the features of this dashboard, take a guided tour
          around the website by clicking the button. This tour will not take
          long and familiarize you with all the core functionalities that this
          dashboard has to offer. You can end the tour at any time by clicking
          'end'. When you reach the end of the tour, the tour will automaticly
          finish.
        </p>
      </div>

      <Search
        tour="step-search"
        update={(query) => navigate('/data?q=' + query)}
      />

      <div className="med-content-container">
        <h1>About This Dashboard</h1>
        <hr className="med-top-separator" />
        <p>
          This software development project is a collaboration between Utrecht
          University (UU) and the Dutch Medicines Evaluation Board (MEB), also
          known as College ter Beoordeling van Geneesmiddelen (CBG). The goal of
          the project is to make data on medicines regulation and marketing
          approval openly available. Currently, data on medicines regulation in
          Europe and beyond is often dispersed across multiple sources. This
          includes for instance relevant data on the regulatory approval of
          medicines for rare diseases, innovative gene- and cell-based therapies
          and approvals of vaccines to treat Covid-19. The project aims to use
          data published by the European Medicines Agency (EMA), the United
          States Food and Drug Administration (US FDA) and the European
          Commission (EC) to create an interactive dashboard to allow intuitive
          visualization and make quantitative analyses of these data easier and
          more consistent.
        </p>
      </div>

      <div className="med-content-container med_content__container">
        <h1>About Us</h1>
        <hr className="med-top-separator" />

        <div>
          <h2>Utrecht University</h2>
          <img src={uuLogo} alt="UU logo" className="institution-logo" />
          <p className="institution-info">
            The Utrecht University team (Jarno Hoekman and Lourens Bloem)
            comprises a collaboration between the Copernicus Institute of
            Sustainable Development (Hoekman) and the Utrecht Institute for
            Pharmaceutical Sciences (Bloem) to make data on the development,
            innovation and regulation of medicines from a pharmaceutical and
            innovation science perspective openly available. In addition,
            Lourens Bloem is affiliated to the Utrecht Science Park foundation,
            in which capacity he is responsible for supporting academic
            activities (especially those related to the life sciences) for which
            the medicines regulatory perspective is relevant.
          </p>
        </div>

        <div>
          <h2>Medicine Evaluation Board</h2>
          <img src={mebLogo} alt="MEB logo" className="institution-logo" />
          <p className="institution-info">
            The MEB is a governmental agency and is under the authority of the
            ministry of Health, Welfare and Sport (Volksgezondheid, Welzijn en
            Sport). The MEB is the responsible authority in the Netherlands for
            regulating medicinal products and assesses medicines for both humans
            and animals on their efficacy, safety (adverse reactions and risks)
            and quality. It is part of the European network of regulatory
            agencies and collaborates with the EMA. See{' '}
            <a
              href="https://cbg-meb.nl/"
              target="_blank"
              rel="noreferrer"
              className="institution-link"
            >
              the MEB website
            </a>{' '}
            for more information. The MEB team consists of the MEBs science
            program manager (Marjon Pasmooij) and a data scientist (Stefan
            Verweij).
          </p>
        </div>
      </div>

      <div className="med-content-container med_content__container">
        <h1>Non Affiliated Regulatory Institutions</h1>
        <hr className="med-top-separator" />
        <h2>European Medicines Agency</h2>

        <p>
          The European Medicines Agency (EMA) is the European agency that
          coordinates the evaluation of centrally authorized medicinal products.
          The EMA functions as the secretariat, and the assessment is performed
          by the individual member states. For each procedure always two
          countries are in the lead. The Netherlands (MEB) is the member state
          with the highest number of procedures each year out of the 27
          countries participating in this collaborative EU regulatory network.
          Medicinal products that have to use the central route of registration
          through the EMA are for instance: cell- and gene therapies, medicinal
          products for oncology, and medicinal products for rare diseases. There
          are also other registration routes, i.e. decentralized/mutual
          recognition through which a company can choose to authorize their
          product in a selection of countries, and lastly, the national route.
          For more information see{' '}
          <a
            href="https://www.ema.europa.eu"
            target="_blank"
            rel="noreferrer"
            className="institution-link"
          >
            the EMA website
          </a>
          .
        </p>

        <h2>European Commission</h2>

        <p>
          The European Commission (EC) is responsible for proposing new laws and
          regulations in the European Union, as well as enforcing the current
          legislation. The EC is owner of the Union Register (in this project
          also referred to as “Community Register”) which lists all medicinal
          products for human and veterinary use that have received a marketing
          authorization decision by the EC through the centralized procedure.
          For more information see{' '}
          <a
            href="https://ec.europa.eu/health/documents/community-register_en"
            target="_blank"
            rel="noreferrer"
            className="institution-link"
          >
            the Union Register website
          </a>
          .
        </p>
      </div>
    </div>
  )
}

export default HomePage
