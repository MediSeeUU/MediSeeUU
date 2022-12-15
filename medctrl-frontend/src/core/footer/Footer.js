// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'
import { NavLink } from 'react-router-dom'
import './Footer.css'

// Function based component rendering the footer
function Footer() {
  return (
    // Footer components, gives the information to be placed in the footer in two sections placed
    // next to each other
    <footer className="med-footer">
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
          . &copy; Utrecht University (ICS)
        </p>
      </section>

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

      <div class="med-footer-github-button">
        <a
          href="https://github.com/MediSeeUU/MediSeeUU/issues"
          target="_blank"
          title="Incorrect data or bug in website?\nClick here to raise a Github issue"
          rel="noreferrer"
        >
          <svg
            width="40px"
            height="40px"
            viewBox="0 0 40 40"
            id="github_button"
            xmlns="http://www.w3.org/2000/svg"
          >
            <title>
              Incorrect data or bug in website? &#10;&#13;Click here to raise a
              Github issue
            </title>
            <g id="exclamation-circle-Regular">
              <path
                id="exclamation-circle-Regular-2"
                data-name="exclamation-circle-Regular"
                d="M20 3.75A16.25 16.25 0 1 0 36.25 20 16.268 16.268 0 0 0 20 3.75Zm0 30A13.75 13.75 0 1 1 33.75 20 13.765 13.765 0 0 1 20 33.75ZM21.667 26.667a1.667 1.667 0 1 1 -1.667 -1.667A1.667 1.667 0 0 1 21.667 26.667Zm-2.917 -6.667V13.333a1.25 1.25 0 0 1 2.5 0v6.667a1.25 1.25 0 0 1 -2.5 0Z"
              />
            </g>
          </svg>
        </a>
      </div>
    </footer>
  )
}

export default Footer
