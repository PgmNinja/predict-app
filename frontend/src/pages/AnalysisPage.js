import React, { useState, useEffect } from 'react';

const AnalysisPage = ({history}) => {
  let [analysis, setAnalysis] = useState(null)

  useEffect(() => {
    getAnalysis()
  }, [])


  let getAnalysis = async () => {
    let response = await fetch('http://localhost:8000/api/analysis/')
    let data = await response.json()
    console.log('Data:', data)
  }


  return <div>
      <h1>Analysis Page</h1>
  </div>;
};

export default AnalysisPage;
