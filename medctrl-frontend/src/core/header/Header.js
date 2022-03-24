import './Header.css';
import logo from '../../images/logo.png'


function Header() {
  return (
    // Header component, contains just the text above the page and the logo. Most work done in the CSS file.
    <header>
      <h1>
          European Database for Medicines Research
      
      </h1>
      <img src={logo} alt='Dashboard logo' id='header__logo'></img>

    </header>
  )
}

export default Header;