// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'
import './Header.css'
import logo from '../../images/logo.svg'
import { Link, NavLink, Router } from 'react-router-dom'

// Function based component rendering the header of the site
function Header() {
  return (
    // Renders the text above the page and the logo
    // Most work is done in the CSS file
    <header className="med-main-header">


      <Link to='/'>
        <div>
          <img
            src={logo}
            alt="Logo of the European Database For Pharmaceutical Policy website "
            id="header__logo"
          />
        </div>
      </Link>

      <h1>European Medicines Regulatory Database</h1>
      <div class="med-header-github-button">
        <a
          href="https://github.com/MediSeeUU/MediSeeUU/issues"
          target="_blank"
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
    </header>
  )
}

export default Header
