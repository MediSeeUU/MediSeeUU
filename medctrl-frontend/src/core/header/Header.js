// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'
import './Header.css'
import logo from '../../images/logo.svg'

// Function based component rendering the header of the site
function Header() {
  return (
    // Renders the text above the page and the logo
    // Most work is done in the CSS file
    <header className="med-main-header">
      <img
        src={logo}
        alt="Logo of the European Database For Pharmaceutical Policy website "
        id="header__logo"
      ></img>
      <h1>European Medicines Regulatory Database</h1>

    </header>
  )
}

export default Header
