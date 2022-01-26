import React, { useState} from 'react';
import teams from '../assets/teams';
import { PieChart, Pie, Legend, Tooltip } from "recharts";

const PredictionPage = ({history}) => {
    let [homeTeam, setHomeTeam] = useState("")
    let [awayTeam, setAwayTeam] = useState("")
    let [result, setResult] = useState("")
    let [home, setHome] = useState("")
    let [away, setAway] = useState("")
    let [homeProba, setHomeProba] = useState(null)
    let [awayProba, setAwayProba] = useState(null)
    let [drawProba, setDrawProba] = useState(null)

    let data01 = [
        { name: home, value: homeProba },
        { name: away, value: awayProba },
        { name: "Draw", value: drawProba},
      ];

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
            setHomeProba(data.probability.home_team)
            setAwayProba(data.probability.away_team)
            setDrawProba(data.probability.draw)
            setHome(data.home_team)
            setAway(data.away_team)
           })
    }

    let handleSubmit = () => {
        predictResult()
        history.push('/')
    }

    return <div>
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
                <button className='btn btn-secondary' onClick={handleSubmit}>Predict</button>
            </div>
                
             
            {result ? (
               <div className='status'>
                    <p className='lead'>{result.result}</p>
                    <h4 className='text-secondary'>Winning Probability</h4>
                    <PieChart width={1000} height={400}>
                        <Pie
                            dataKey="value"
                            isAnimationActive={false}
                            data={data01}
                            cx={200}
                            cy={200}
                            outerRadius={80}
                            fill="#63686b"
                            label
                        />
                        <Tooltip />
                    </PieChart>
                </div>
                
            ): ( 
            <div className='status'>
                <p className='lead'>{result.result}</p>
            </div>
            )} 
         </div>;
    };

export default PredictionPage;