import './Footer.css'

function Footer() {
  return (
    //Footer components, gives the information to be placed in the footer in two sections placed
    //next to each other.
    <footer className="med_footer">
      <section id="footer__organizations">
        <h2>Relevant Organizations</h2>

        <ul className="footer__organization__list">
          <li>
            {' '}
            <a
              className="footer__list__link"
              href="https://english.cbg-meb.nl/"
            >
              Medicines Evaluation Board
            </a>
          </li>
          <li>
            {' '}
            <a className="footer__list__link" href="https://www.uu.nl/en">
              Utrecht University
            </a>
          </li>
        </ul>
      </section>

      <section id="footer__information">
        <p className="footer-text">
          In the European Database For Pharmaceutical Policy & Regulation, data
          on medicines regulation and marketing approval is made available. The
          dashboard, including the data collection, is maintained by Utrecht
          University and the Dutch Medicines Evaluation Board. For more
          information please visit the{' '}
          <a className="footer__list__link" href="/info">
            info page
          </a>
          .
        </p>
      </section>
    </footer>
  )
}

export default Footer
