import './App.css';
import { 
  BrowserRouter as Router,
  Route     
} from 'react-router-dom'

import Header from './components/Headers';
import PredictionPage from './pages/PredictionPage';
import AnalysisPage from './pages/AnalysisPage';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <Route path="/" exact component={PredictionPage} />
        <Route path="/analysis" component={AnalysisPage} />
      </div>
    </Router>
  );
}

export default App;
