import './App.css';
import { 
  BrowserRouter as Router,
  Route     
} from 'react-router-dom'

import Header from './components/Headers';
import PredictionPage from './pages/PredictionPage';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <Route path="/" exact component={PredictionPage} />
      </div>
    </Router>
  );
}

export default App;
