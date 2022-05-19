import { NavLink } from 'react-router-dom'
import './Footer.css'

function Footer() {
  return (
    //Footer components, gives the information to be placed in the footer in two sections placed
    //next to each other.
    <footer className="med-footer">
      <section id="med-footer-organizations">
        <h2>Relevant Organizations</h2>

        <ul className="med-footer-organization-list">
          <li>
            {' '}
            <a className="med-link" href="https://english.cbg-meb.nl/">
              Medicines Evaluation Board
            </a>
          </li>
          <li>
            {' '}
            <a className="med-link" href="https://www.uu.nl/en">
              Utrecht University
            </a>
          </li>
        </ul>
      </section>

      <section id="med-footer-information">
        <p className="med-footer-text">
          In the European Database For Pharmaceutical Policy & Regulation, data
          on medicines regulation and marketing approval is made available. The
          dashboard, including the data collection, is maintained by Utrecht
          University and the Dutch Medicines Evaluation Board. For more
          information please visit the{' '}
          <NavLink className="med-link" to="/info">
            info page
          </NavLink>
          .
        </p>
      </section>
    </footer>
  )
}

export default Footer
