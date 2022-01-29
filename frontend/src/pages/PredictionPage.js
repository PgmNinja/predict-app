import React, { useState} from 'react';
import teams from '../assets/teams';
import { Link } from "react-router-dom"
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
  } from 'chart.js';
  import { Pie } from 'react-chartjs-2';
  
  ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
  );

const PredictionPage = ({history}) => {
    let [homeTeam, setHomeTeam] = useState("")
    let [awayTeam, setAwayTeam] = useState("")
    let [result, setResult] = useState("")
    let [home, setHome] = useState("")
    let [away, setAway] = useState("")
    let [proba, setProba] = useState([])


    const data01 = {
        labels: [home, away, "Draw"],
        datasets: [
          {
            label: '# of Votes',
            data: proba,
            backgroundColor: [
              "#00aba9",
              "#742774",
              "#494d4f"
            ],
  
            borderWidth: 1,
          },
        ],
      };
  

    let predictResult = async () => {
        fetch('http://127.0.0.1:8000/api/predict/', {
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
            setResult(data);
            setProba(data.probability)
            setHome(data.home_team)
            setAway(data.away_team)
           })
    }

    let handleSubmit = () => {
        localStorage.setItem('homeTeam', homeTeam)
        localStorage.setItem('awayTeam', awayTeam)
        predictResult()
        history.push('/')
    }

    return <div>
        <h3 className='analysis'>Let's Predict...</h3>
            <div  className='select-menu'>
                <select className='form-select' onChange={(e)=>{
                    const selectedHomeTeam=e.target.value;
                    setHomeTeam(selectedHomeTeam)
                }}>
                    {teams.map(team => (
                        <option value={team.team}>{team.team}</option>
                    ))}                
                </select>

            </div>

            <div  className='select-menu'>
                <select className='form-select' onChange={(e)=>{
                    const selectedawayTeam=e.target.value;
                    setAwayTeam(selectedawayTeam)
                }}>
                    {teams.map(team => (
                        <option value={team.team}>{team.team}</option>
                    ))}
                </select>
            </div>
            <div className='select-menu'>
                <button className='btn btn-success' onClick={handleSubmit}>Predict</button>
            </div>
                
             
            {result ? (
               <div className='status'>
                    <p className='lead'>{result.result}</p>
                    <h4 className='text-secondary'>Winning Probability</h4>
                    <div className='pie-diagram'>
                    <Pie data={data01} />
                    </div>
                    <Link className='link' to={'/analysis'}>See analysis</Link>
                </div>
                
            ): ( 
            <div className='status'>
                <p className='lead'>{result.result}</p>
            </div>
            )} 
         </div>;
    };

export default PredictionPage;