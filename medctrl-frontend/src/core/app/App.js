import './App.css';
import {BrowserRouter} from 'react-router-dom';
import SideNavigation from '../navigation/Navigation';
import AllRoutes from "../routes/AllRoutes.js";

const userLoggedIn = true;
const defUser = {
  isAdmin: true,
  userName: 'Lourens Bloem',
  accessLevel: 'X'
}

function App() {
  return (
    <BrowserRouter>
      <header>
        <h1>
          European Medinice Data Dashboard
        </h1>
      </header>
      <SideNavigation loggedin={userLoggedIn} user={defUser}/>
      <main className='content'>
        <AllRoutes />
        <footer>
          <h3>Footer</h3>
        </footer>
      </main>
    </BrowserRouter>
  );
}

export default App;