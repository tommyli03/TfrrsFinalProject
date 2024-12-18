import React, { useState, useEffect } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";

const XC5KAnalysis = () => {
  const [analysisData, setAnalysisData] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:5000/xc_2024_5k_analysis")
      .then((response) => setAnalysisData(response.data))
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  return (
    <div className="container mt-5">
      <h1 className="mb-4">2024 XC 5K Analysis</h1>
      <table className="table table-striped">
        <thead>
          <tr>
            <th>Team</th>
            <th>Average 5K Time</th>
            <th>5K Rank</th>
            <th>Meet Rank</th>

          </tr>
        </thead>
        <tbody>
          {analysisData.map((row, index) => (
            <tr key={index}>
              <td>{row.team}</td>
              <td>{row.avg_5k_time_mm_ss}</td>
              <td>{row.team_5k_rank}</td>
              <td>{row.meet_rank}</td>
 
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default XC5KAnalysis;
