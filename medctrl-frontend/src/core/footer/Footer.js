import './Footer.css'

function Footer() {
  return (
    //Footer components, gives the information to be placed in the footer in two sections placed
    //next to each other.
    <footer>
      <section id="footer__organisations">
        <h2>Relevant organisations</h2>

        <ul className="footer__organisation__list">
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
              University of Utrecht
            </a>
          </li>
        </ul>
      </section>

      <section id="footer__information">
        <h2>General information</h2>

        <p>
          This is a development version of the dashboard created for the
          Medicines Evaluation Board. For questions and remarks regarding this
          website, please visit the <b>contact</b> page.
        </p>
      </section>
    </footer>
  )
}

export default Footer
