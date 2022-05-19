import './Header.css'
import logo from '../../images/logo.svg'

function Header() {
  return (
    // Header component, contains just the text above the page and the logo.
    // Most work is done in the CSS file.
    <header className="med-main-header">
      <h1>European Database For Pharmaceutical Policy &amp; Regulation</h1>
      <img src={logo} alt="Dashboard logo" id="header__logo"></img>
    </header>
  )
}

export default Header
