import React, { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js';
import { Line, Pie, Bar } from 'react-chartjs-2';
import * as ReactBootStrap from 'react-bootstrap'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  BarElement,
);



const AnalysisPage = ({history}) => {
  
  let [loading, setLoading] = useState(false)
  let [homeTeam, setHomeTeam] = useState("")
  let [awayTeam, setAwayTeam] = useState("")
  let [homeStats, setHomeStats] = useState([])
  let [awayStats, setAwayStats] = useState([])
  let [years, setYears] = useState([])
  let [headtToHead, setHeadToHead] = useState([])
  let [polarity, setPolarity] = useState([])

    useEffect(() => {
    getData()
    analysisResult()  
    }, [])

    let getData = () => {
      homeTeam = localStorage.getItem('homeTeam', homeTeam)
      awayTeam = localStorage.getItem('awayTeam', awayTeam)
      setHomeTeam(homeTeam)
      setAwayTeam(awayTeam)
    }

 

  const data01 = {
      labels: years,
      datasets: [
        {
          label: homeTeam,
          data: homeStats,
          fill: false,
          borderColor: "rgba(75,192,192,1)"
        },
        {
          label:awayTeam,
          data: awayStats,
          fill: false,
          borderColor: "#742774"
        }
      ]
    };

    const data02 = {
      labels: [homeTeam, awayTeam],
      datasets: [
        {
          label: '# of Votes',
          data: headtToHead,
          backgroundColor: [
            "rgba(75,192,192,1)",
            "#742774"
          ],

          borderWidth: 1,
        },
      ],
    };
    const labels = [homeTeam, awayTeam]
    const data03 = {
      labels,
      datasets: [
        {
          label: 'Polarity',
          data: polarity,
          backgroundColor: '#00aba9',
        },
    
      ],
    };



  
  
  let analysisResult = async () => {
    setLoading(true)
    fetch('http://127.0.0.1:8000/api/analysis/', {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "home_team": homeTeam,
            "away_team": awayTeam
        })
    }).then(function(response) {
      return response.json();
     })
     .then(function(data) {
      console.log('Result:', data)

      setHomeStats(data.home_win_stats)
      setAwayStats(data.away_win_stats)
      setYears(data.years)
      setHeadToHead(data.count)
      setPolarity(data.polarity)
      setLoading(false)

     })
}
 

  return <div>
    {loading ? (<div className='spinner'><ReactBootStrap.Spinner animation="border" /></div>): (
        <div>
          <h1 className='analysis'>Analysis</h1>
          <h3 className='analysis-1'>Performance over Years</h3>
          <div className="line-diagram">
            <Line data={data01} />
          </div>
          <h3 className='analysis-1'>Head to Head Analysis</h3>
          <div className='pie-diagram'>
            <Pie data={data02} />
          </div>
          <h3 className='analysis-1'>Support on Twitter</h3>
          <div className='line-diagram'>
            <Bar data={data03} />
          </div>
      </div>
    )}
      

    </div>

};

export default AnalysisPage;
