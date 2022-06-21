// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import './Header.css'
import logo from '../../images/logo.svg'

// Function based component rendering the header of the site
function Header() {
  return (
    // Renders the text above the page and the logo
    // Most work is done in the CSS file
    <header className="med-main-header">
      <h1>European Database For Pharmaceutical Policy &amp; Regulation</h1>
      <img src={logo} alt="Dashboard logo" id="header__logo"></img>
    </header>
  )
}

export default Header
